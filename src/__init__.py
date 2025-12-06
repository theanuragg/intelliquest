"""
IntelliQuest - AI Document Automation Engine

An intelligent, end-to-end agentic system that autonomously automates browser tasks,
downloads documents, performs OCR, and extracts structured data using local AI models.

Key Features:
    - Autonomous browser automation using Playwright
    - Local AI reasoning with Fara-7B via Ollama
    - Document download and OCR processing with Tesseract
    - Smart text cleaning and error correction
    - Self-correcting agentic loop (Reason → Act → Observe → Update)
    - Structured data extraction to JSON with schema validation
    - Comprehensive audit logging and traceability
    - REST API for task management via FastAPI
    - Modern web dashboard for monitoring and control
    - 100% local processing - no cloud dependencies

Architecture:
    The system consists of several key components:
    
    - BrowserController: Playwright-based browser automation
    - FaraReasoningEngine: AI reasoning using Fara-7B via Ollama
    - OCRProcessor: Tesseract-based text extraction from documents
    - DocumentPipeline: End-to-end document processing workflow
    - AutomationOrchestrator: Main agentic loop coordinator
    - FastAPI Server: REST API and task management interface

Typical Use Cases:
    - Automated invoice download and data extraction
    - Multi-step form filling and submission
    - Document classification and processing
    - Web scraping with intelligent navigation
    - Compliance-focused audit trail generation

Example:
    >>> from src.agent.orchestrator import AutomationOrchestrator
    >>> orchestrator = AutomationOrchestrator()
    >>> task = orchestrator.create_task(
    ...     objective="Login to portal, download invoice, extract vendor and amount"
    ... )
    >>> orchestrator.execute_task(task.task_id)

Dependencies:
    - Ollama with Fara-7B model
    - Python 3.9+
    - Playwright (Chromium)
    - Tesseract OCR
    - FastAPI for REST API
    - Various Python libraries (see requirements.txt)

For more information, see:
    - README.md: Comprehensive documentation
    - START_HERE.md: Quick start guide
    - INSTALLATION.md: Setup instructions
"""

# Main package
__version__ = "1.0.0"
__author__ = "AI Automation Team"
