from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import json
from pathlib import Path

from src.agent.orchestrator import AutomationOrchestrator
from src.config import API_HOST, API_PORT, API_DEBUG
from src.utils.logger import get_logger

logger = get_logger("api_server")

# Global orchestrator instance
orchestrator: Optional[AutomationOrchestrator] = None


# Pydantic models
class TaskRequest(BaseModel):
    """Request model for creating automation tasks"""
    objective: str
    params: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    """Response model for task operations"""
    task_id: str
    status: str
    created_at: str = None


class TaskStatusResponse(BaseModel):
    """Response model for task status"""
    task_id: str
    status: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    num_actions: int = 0


# Create FastAPI app
app = FastAPI(
    title="AI Document Automation Engine",
    description="Autonomous browser automation + OCR using Fara-7B",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize orchestrator on startup"""
    global orchestrator
    logger.info("Starting API server...")
    orchestrator = AutomationOrchestrator()
    await orchestrator.initialize()
    logger.info("API server ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global orchestrator
    if orchestrator:
        await orchestrator.shutdown()
    logger.info("API server shutdown")


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Document Automation Engine",
        "model": "Fara-7B (via Ollama)"
    }


# Task management endpoints
@app.post("/tasks")
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks) -> TaskResponse:
    """Create and execute a new automation task"""
    global orchestrator

    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    # Create task
    task_id = orchestrator.create_task(request.objective, request.params)
    logger.info(f"Created task: {task_id}")

    # Execute in background
    background_tasks.add_task(orchestrator.execute_task, task_id)

    return TaskResponse(
        task_id=task_id,
        status="queued",
        created_at=None
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """Get status of a specific task"""
    global orchestrator

    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    status = orchestrator.get_task_status(task_id)
    if status.get("status") == "error":
        raise HTTPException(status_code=404, detail=status.get("error"))

    return TaskStatusResponse(**status)


@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str) -> Dict[str, Any]:
    """Get result of a completed task"""
    global orchestrator

    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    task_status = orchestrator.get_task_status(task_id)
    if task_status.get("status") == "error":
        raise HTTPException(status_code=404, detail="Task not found")

    if task_status.get("status") not in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Task not yet completed")

    task = orchestrator.tasks.get(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result,
        "error": task.error,
        "extracted_data": task.extracted_data,
    }


@app.get("/tasks/{task_id}/audit")
async def get_task_audit_log(task_id: str) -> List[Dict[str, Any]]:
    """Get detailed audit log for a task"""
    global orchestrator

    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    audit_log = orchestrator.get_task_audit_log(task_id)
    if audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log not found")

    return audit_log


@app.get("/tasks")
async def list_tasks() -> List[Dict[str, Any]]:
    """List all tasks"""
    global orchestrator

    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")

    return [task.to_dict() for task in orchestrator.tasks.values()]


# File management endpoints
@app.get("/downloads")
async def list_downloads() -> List[Dict[str, Any]]:
    """List downloaded files"""
    from src.config import DOWNLOADS_DIR

    downloads_dir = Path(DOWNLOADS_DIR)
    if not downloads_dir.exists():
        return []

    files = []
    for filepath in downloads_dir.glob("*.*"):
        if filepath.is_file():
            files.append({
                "name": filepath.name,
                "size": filepath.stat().st_size,
                "created": filepath.stat().st_ctime,
            })

    return files


@app.get("/downloads/{filename}")
async def download_file(filename: str):
    """Download a specific file"""
    from src.config import DOWNLOADS_DIR

    filepath = Path(DOWNLOADS_DIR) / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=filepath, filename=filename)


# System info endpoints
@app.get("/system/config")
async def get_system_config() -> Dict[str, Any]:
    """Get system configuration (non-sensitive)"""
    from src.config import (
        OLLAMA_BASE_URL,
        OLLAMA_MODEL,
        BROWSER_HEADLESS,
        MAX_RETRIES,
    )

    return {
        "ollama_url": OLLAMA_BASE_URL,
        "model": OLLAMA_MODEL,
        "browser_headless": BROWSER_HEADLESS,
        "max_retries": MAX_RETRIES,
    }


@app.get("/system/logs")
async def get_system_logs(lines: int = 50) -> Dict[str, Any]:
    """Get recent system logs"""
    from src.config import LOG_DIR

    log_files = list(Path(LOG_DIR).glob("*.log"))
    if not log_files:
        return {"logs": []}

    # Read the most recent log file
    latest_log = max(log_files, key=lambda p: p.stat().st_mtime)

    try:
        with open(latest_log, "r") as f:
            log_lines = f.readlines()[-lines:]
        return {
            "log_file": latest_log.name,
            "logs": log_lines,
        }
    except Exception as e:
        return {"error": str(e)}


def run_server():
    """Run the FastAPI server"""
    import uvicorn

    logger.info(f"Starting server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        debug=API_DEBUG,
    )


if __name__ == "__main__":
    run_server()
