import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DOWNLOADS_DIR = BASE_DIR / os.getenv("DOWNLOAD_DIR", "downloads")
CACHE_DIR = BASE_DIR / os.getenv("CACHE_DIR", "cache")
LOG_DIR = BASE_DIR / os.getenv("LOG_DIR", "logs")

# Create directories if they don't exist
DOWNLOADS_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "fara-7b")

# Website Credentials
TARGET_WEBSITE_URL = os.getenv("TARGET_WEBSITE_URL")
TARGET_USERNAME = os.getenv("TARGET_USERNAME")
TARGET_PASSWORD = os.getenv("TARGET_PASSWORD")

# Browser Settings
BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "True").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
BROWSER_VIEWPORT_WIDTH = int(os.getenv("BROWSER_VIEWPORT_WIDTH", "1280"))
BROWSER_VIEWPORT_HEIGHT = int(os.getenv("BROWSER_VIEWPORT_HEIGHT", "720"))

# System Settings
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
INFERENCE_TIMEOUT = int(os.getenv("INFERENCE_TIMEOUT", "120"))

# Tesseract
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "/usr/local/bin/tesseract")

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"

# Fara-7B Context and Inference Parameters
FARA_CONTEXT_WINDOW = 4096
FARA_TEMPERATURE = 0.7
FARA_TOP_P = 0.9
FARA_TOP_K = 40
FARA_REPEAT_PENALTY = 1.1
