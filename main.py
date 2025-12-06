#!/usr/bin/env python3
"""
Main entry point for the IntelliQuest AI Document Automation Engine

This module serves as the primary entry point for starting the FastAPI server
that powers the IntelliQuest automation system. It provides a REST API for
creating and managing automation tasks, monitoring their execution, and
accessing results.

What IntelliQuest Does:
    IntelliQuest is an autonomous AI-powered system that:
    
    1. Browser Automation:
       - Logs into websites using provided credentials
       - Navigates complex user interfaces intelligently
       - Clicks buttons, fills forms, and interacts with web elements
       - Handles dynamic content and JavaScript-heavy pages
    
    2. Document Processing:
       - Downloads documents (PDF, images, etc.)
       - Extracts text using OCR (Tesseract)
       - Cleans and normalizes extracted text
       - Classifies document types using AI
    
    3. Data Extraction:
       - Converts unstructured text to structured JSON
       - Validates against user-defined schemas
       - Extracts specific fields (invoice numbers, amounts, dates, etc.)
       - Maintains high accuracy through AI reasoning
    
    4. Self-Correction:
       - Detects when actions fail
       - Uses Fara-7B to analyze errors and suggest fixes
       - Retries with corrected selectors or strategies
       - Learns from failures during execution
    
    5. Audit & Compliance:
       - Logs every action taken in detailed JSON format
       - Maintains complete audit trails for compliance
       - Timestamps all operations for traceability
       - Provides comprehensive error reporting

System Architecture:
    The system operates on an agentic loop:
    
    Observe → Reason → Act → Update → (repeat)
    
    Where:
    - Observe: Capture current page state (HTML, URL, screenshots)
    - Reason: Fara-7B analyzes state and plans next actions
    - Act: Execute actions via Playwright (click, fill, navigate)
    - Update: Log results, process downloads, extract data

Prerequisites:
    - Ollama running locally with Fara-7B model loaded
    - Python 3.9 or higher
    - Tesseract OCR installed and accessible
    - Playwright browsers installed (Chromium)

Usage:
    Direct execution:
        $ python main.py
    
    Via helper script:
        $ bash start.sh
    
    The server will start on http://localhost:8000 with:
        - REST API endpoints at http://localhost:8000/tasks, /downloads, etc.
        - Web dashboard at http://localhost:8000/frontend/index.html
        - Health check at http://localhost:8000/health

API Endpoints:
    POST   /tasks              - Create a new automation task
    GET    /tasks              - List all tasks
    GET    /tasks/{id}         - Get task status
    GET    /tasks/{id}/result  - Get task results
    GET    /tasks/{id}/audit   - Get audit log for task
    GET    /downloads          - List downloaded files
    GET    /downloads/{file}   - Download a specific file
    GET    /health             - System health check

Example Task:
    curl -X POST http://localhost:8000/tasks \\
      -H "Content-Type: application/json" \\
      -d '{
        "objective": "Login to accounting portal, download latest invoice, 
                      extract vendor name and total amount",
        "params": {"wait_for_download": true}
      }'

Environment Configuration:
    Configure via .env file:
    - OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434)
    - OLLAMA_MODEL: Model to use (default: fara-7b)
    - TARGET_WEBSITE_URL: Website to automate
    - TARGET_USERNAME: Login username
    - TARGET_PASSWORD: Login password
    - BROWSER_HEADLESS: Run browser in headless mode (default: True)
    - And many more (see .env.example)

For More Information:
    See README.md, START_HERE.md, and INSTALLATION.md for comprehensive
    documentation on features, setup, and usage.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.api.server import run_server
from src.utils.logger import get_logger

logger = get_logger("main")


def main():
    """Run the API server"""
    logger.info("Starting AI Document Automation Engine")
    logger.info("Make sure Ollama is running with Fara-7B model")
    logger.info("API available at http://localhost:8000")
    logger.info("Dashboard available at http://localhost:8000/frontend/index.html")

    try:
        run_server()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
