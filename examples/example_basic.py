#!/usr/bin/env python3
"""
Example: Basic login and document download automation
"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.agent.orchestrator import AutomationOrchestrator
from src.utils.logger import get_logger

logger = get_logger("example_basic")


async def main():
    """Run a basic automation example"""
    logger.info("Starting basic automation example")

    # Initialize orchestrator
    orchestrator = AutomationOrchestrator()
    await orchestrator.initialize()

    try:
        # Create a task
        task_id = orchestrator.create_task(
            objective="Navigate to https://example.com and take a screenshot",
            params={"headless": True},
        )

        logger.info(f"Created task: {task_id}")

        # Execute task
        result = await orchestrator.execute_task(task_id)

        logger.info(f"Task result: {json.dumps(result, indent=2)}")

        # Get task status
        task_status = orchestrator.get_task_status(task_id)
        logger.info(f"Task status: {json.dumps(task_status, indent=2)}")

        # Get audit log
        audit_log = orchestrator.get_task_audit_log(task_id)
        if audit_log:
            logger.info(f"Audit log entries: {len(audit_log)}")

    finally:
        await orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
