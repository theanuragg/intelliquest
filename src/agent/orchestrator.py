import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from src.browser.controller import BrowserController
from src.reasoning.engine import FaraReasoningEngine
from src.ocr.pipeline import DocumentPipeline
from src.config import MAX_RETRIES
from src.utils.logger import get_logger, AuditLogger

logger = get_logger("agent_orchestrator")


class AutomationTask:
    """Represents a single automation task"""

    def __init__(self, task_id: str, objective: str, params: Dict[str, Any] = None):
        self.task_id = task_id
        self.objective = objective
        self.params = params or {}
        self.status = "pending"
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.completed_actions = []
        self.extracted_data = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "objective": self.objective,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error,
            "num_actions": len(self.completed_actions),
        }


class AutomationOrchestrator:
    """Main agentic system orchestrating browser automation + reasoning + OCR"""

    def __init__(self):
        self.browser = BrowserController()
        self.reasoning_engine = FaraReasoningEngine()
        self.document_pipeline = DocumentPipeline()
        self.tasks: Dict[str, AutomationTask] = {}
        self.audit_logger = None

    async def initialize(self):
        """Initialize all subsystems"""
        logger.info("Initializing AutomationOrchestrator")
        await self.browser.initialize()
        logger.info("Browser initialized")

    async def shutdown(self):
        """Shutdown all subsystems"""
        logger.info("Shutting down AutomationOrchestrator")
        await self.browser.close()

    def create_task(self, objective: str, params: Dict[str, Any] = None) -> str:
        """Create a new automation task"""
        task_id = str(uuid.uuid4())
        task = AutomationTask(task_id, objective, params)
        self.tasks[task_id] = task
        self.audit_logger = AuditLogger(task_id)

        logger.info(f"Created task {task_id}: {objective}")
        return task_id

    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a single task through the agentic loop"""
        if task_id not in self.tasks:
            logger.error(f"Task not found: {task_id}")
            return {"status": "error", "error": "Task not found"}

        task = self.tasks[task_id]
        task.status = "running"
        task.started_at = datetime.utcnow().isoformat()

        try:
            # Main agentic loop: reason -> act -> observe -> update
            result = await self._agentic_loop(task)
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.utcnow().isoformat()

            logger.info(f"Task {task_id} completed successfully")
            return {"status": "success", "task_id": task_id, "result": result}

        except Exception as e:
            logger.error(f"Task {task_id} failed: {str(e)}")
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.utcnow().isoformat()
            return {"status": "error", "task_id": task_id, "error": str(e)}

    async def _agentic_loop(self, task: AutomationTask) -> Dict[str, Any]:
        """Main reason -> act -> observe -> update loop"""
        max_iterations = 20
        iteration = 0

        logger.info(f"Starting agentic loop for task {task.task_id}")

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}/{max_iterations}")

            # Step 1: Observe current page state
            page_state = await self.browser.get_page_state()
            logger.debug(f"Page state: {page_state['title']} - {page_state['url']}")

            # Step 2: Reason about what to do
            reasoning_result = await self.reasoning_engine.generate_browser_actions(
                objective=task.objective,
                page_state=page_state,
                previous_actions=task.completed_actions,
            )

            if reasoning_result.get("status") != "success":
                logger.error(f"Reasoning failed: {reasoning_result.get('error')}")
                return {
                    "status": "error",
                    "reason": "Reasoning failed",
                    "iteration": iteration,
                }

            actions = reasoning_result.get("actions", [])
            if not actions:
                logger.info("No more actions generated, task might be complete")
                return {
                    "status": "success",
                    "reason": "No more actions",
                    "iteration": iteration,
                    "extracted_data": task.extracted_data,
                }

            # Step 3: Execute actions
            for action_idx, action in enumerate(actions):
                logger.info(f"Executing action {action_idx + 1}/{len(actions)}: {action.get('action')}")

                retry_count = 0
                action_result = None

                while retry_count < MAX_RETRIES:
                    action_result = await self.browser.execute_action(action)

                    if action_result.get("status") == "success":
                        logger.info(f"Action succeeded: {action.get('action')}")
                        task.completed_actions.append(action_result)
                        break
                    else:
                        retry_count += 1
                        logger.warning(
                            f"Action failed, retry {retry_count}/{MAX_RETRIES}: {action_result.get('error')}"
                        )

                        # Try self-correction if it's a selector-based action
                        if retry_count < MAX_RETRIES and action.get("selector"):
                            logger.info("Attempting self-correction...")
                            correction = await self.reasoning_engine.self_correct_selector(
                                failed_selector=action.get("selector"),
                                html=page_state.get("html", ""),
                                element_description=action.get("reason", ""),
                            )

                            if correction.get("status") == "success":
                                corrected_selectors = correction.get("corrected_selectors", [])
                                if corrected_selectors:
                                    action["selector"] = corrected_selectors[0]
                                    logger.info(f"Using corrected selector: {action['selector']}")
                                    continue

                        # If still failing, skip and continue
                        if retry_count >= MAX_RETRIES:
                            logger.warning(f"Max retries reached for action: {action.get('action')}")
                            task.completed_actions.append(
                                {
                                    "action": action.get("action"),
                                    "status": "failed",
                                    "error": action_result.get("error"),
                                    "retries": retry_count,
                                }
                            )
                            break

                # Log action to audit
                self.audit_logger.log_action(
                    action_type=action.get("action"),
                    action_data=action,
                    status="success" if action_result and action_result.get("status") == "success" else "failed",
                    error=action_result.get("error") if action_result else None,
                )

            # Step 4: Check if we need to process downloaded documents
            # (This would be triggered by observing new files in download directory)
            await self._check_and_process_downloads(task)

            # Small delay before next iteration
            await asyncio.sleep(1)

        logger.info(f"Agentic loop completed after {iteration} iterations")
        return {
            "status": "success",
            "iterations": iteration,
            "extracted_data": task.extracted_data,
        }

    async def _check_and_process_downloads(self, task: AutomationTask):
        """Check for newly downloaded files and process them"""
        from src.config import DOWNLOADS_DIR

        downloads_dir = Path(DOWNLOADS_DIR)
        if not downloads_dir.exists():
            return

        # Get list of files (simple approach - in production would track processed files)
        files = list(downloads_dir.glob("*.*"))
        if not files:
            return

        logger.info(f"Found {len(files)} files to process")

        for filepath in files[:1]:  # Process one at a time
            if filepath.is_file():
                logger.info(f"Processing downloaded file: {filepath.name}")

                # Process through OCR pipeline
                doc_result = self.document_pipeline.process_document(str(filepath))

                if doc_result.get("status") == "success":
                    # Classify document
                    cleaned_text = doc_result.get("cleaned_text", "")
                    if cleaned_text:
                        classification = await self.reasoning_engine.classify_document(cleaned_text)
                        logger.info(f"Document classified as: {classification.get('doc_type')}")

                        # Extract structured data
                        extraction_schema = {
                            "name": "Full name or entity name",
                            "date": "Date of document",
                            "amount": "Amount or total value",
                            "reference": "Reference or ID number",
                        }

                        extraction = await self.reasoning_engine.extract_information(
                            cleaned_text, extraction_schema
                        )

                        if extraction.get("status") == "success":
                            task.extracted_data[filepath.name] = extraction.get("fields", {})

                            # Log to audit
                            self.audit_logger.log_document_extracted(
                                filename=filepath.name,
                                doc_type=classification.get("doc_type", "unknown"),
                                extracted_fields=extraction.get("fields", {}),
                                confidence=extraction.get("confidence", 0.0),
                            )

                            logger.info(f"Extracted data from {filepath.name}")

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get current status of a task"""
        if task_id not in self.tasks:
            return {"status": "error", "error": "Task not found"}

        task = self.tasks[task_id]
        return task.to_dict()

    def get_task_audit_log(self, task_id: str) -> Optional[list]:
        """Get audit log for a task"""
        log_file = Path(f"logs/audit_{task_id}.json")
        if log_file.exists():
            with open(log_file, "r") as f:
                return json.load(f)
        return None
