import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import sys

from src.config import LOG_DIR


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler - JSON format
    log_file = LOG_DIR / f"{name}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    # Console handler - simple format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


class AuditLogger:
    """Structured audit logging for tracking actions and decisions"""

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.log_file = LOG_DIR / f"audit_{task_id}.json"
        self.logs: list = []

    def log_action(
        self,
        action_type: str,
        action_data: Dict[str, Any],
        status: str = "pending",
        error: Optional[str] = None,
    ):
        """Log an action with metadata"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": action_type,
            "action_data": action_data,
            "status": status,
            "error": error,
        }
        self.logs.append(entry)
        self._write_logs()

    def log_reasoning(
        self,
        input_context: str,
        fara_decision: Dict[str, Any],
        confidence: float,
    ):
        """Log AI reasoning decisions"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "reasoning",
            "input_context": input_context[:500],  # Truncate for readability
            "fara_decision": fara_decision,
            "confidence": confidence,
        }
        self.logs.append(entry)
        self._write_logs()

    def log_document_extracted(
        self,
        filename: str,
        doc_type: str,
        extracted_fields: Dict[str, Any],
        confidence: float,
    ):
        """Log document extraction results"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "document_extracted",
            "filename": filename,
            "doc_type": doc_type,
            "fields": extracted_fields,
            "confidence": confidence,
        }
        self.logs.append(entry)
        self._write_logs()

    def log_workflow_decision(
        self,
        current_state: str,
        next_step: str,
        reasoning: str,
        confidence: float,
    ):
        """Log workflow routing decisions"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "workflow_decision",
            "current_state": current_state,
            "next_step": next_step,
            "reasoning": reasoning,
            "confidence": confidence,
        }
        self.logs.append(entry)
        self._write_logs()

    def _write_logs(self):
        """Write logs to JSON file"""
        with open(self.log_file, "w") as f:
            json.dump(self.logs, f, indent=2)

    def get_logs(self) -> list:
        """Get all logs"""
        return self.logs
