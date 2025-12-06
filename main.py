#!/usr/bin/env python3
"""
Main entry point for the AI Document Automation Engine
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
