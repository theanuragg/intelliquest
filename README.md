# 🤖 AI Document Automation Engine

**Intelligent browser automation + document extraction system using Fara-7B (local)**

A complete end-to-end agentic system that autonomously logs into websites, navigates UI, downloads documents, runs OCR, and extracts structured data—all locally using Fara-7B.

---

## 📋 Features

✅ **Autonomous Browser Automation** - Playwright-based automation with Fara-7B reasoning
✅ **Document Download & OCR** - Extract text from PDF, JPG, PNG, TIFF with Tesseract
✅ **Smart Text Cleaning** - Automatic OCR error correction and normalization
✅ **Agentic Loop** - Reason → Act → Observe → Update cycle
✅ **Self-Correction** - Fara-7B proposes corrected selectors when actions fail
✅ **Structured Extraction** - Convert extracted text to JSON with schema
✅ **Comprehensive Logging** - Deep audit trails in JSON format
✅ **FastAPI Server** - REST API for task management
✅ **Web Dashboard** - Modern UI for monitoring and control
✅ **100% Local** - No cloud, no external API calls

---

## 🛠 Prerequisites

1. **Ollama** (running locally)
   ```bash
   # Install from https://ollama.ai
   # Then pull Fara-7B:
   ollama pull fara-7b
   # Start Ollama (usually runs as background service)
   ollama serve
   ```

2. **Python 3.9+**
   ```bash
   python --version  # Verify installation
   ```

3. **Tesseract OCR**
   ```bash
   # macOS
   brew install tesseract

   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr

   # Windows
   # Download installer: https://github.com/UB-Mannheim/tesseract/wiki
   ```

4. **Playwright Browsers**
   ```bash
   playwright install chromium
   ```

---

## 📦 Installation

1. **Clone/Navigate to project:**
   ```bash
   cd /Users/anurag/coding/projects/quest
   ```

2. **Create Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install additional dependencies:**
   ```bash
   # For PDF support
   pip install pdf2image
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings:
   # - TARGET_WEBSITE_URL
   # - TARGET_USERNAME
   # - TARGET_PASSWORD
   # - TESSERACT_PATH (if different from default)
   ```

6. **Verify Tesseract installation:**
   ```bash
   which tesseract  # Find path
   # Update TESSERACT_PATH in .env if needed
   ```

---

## 🚀 Quick Start

### 1. Start Ollama (in separate terminal)
```bash
ollama serve
# Verify Fara-7B is loaded:
curl http://localhost:11434/api/tags | grep fara-7b
```

### 2. Start the API Server
```bash
cd /Users/anurag/coding/projects/quest
source venv/bin/activate
python main.py
```

Server will start on `http://localhost:8000`

### 3. Open Dashboard
```bash
# In your browser:
http://localhost:8000/frontend/
```

### 4. Create a Task

Via **Web Dashboard:**
1. Enter objective (e.g., "Login to example.com with credentials, navigate to downloads, download invoice, extract data")
2. Click "Create & Execute Task"
3. Monitor progress in real-time

Via **API:**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Login to example.com and download documents",
    "params": {
      "wait_for_download": true
    }
  }'
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2025-12-06T10:30:00Z"
}
```

### 5. Monitor Task Status

```bash
# Check status
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000

# Get results
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000/result

# Get audit log
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000/audit
```

---

## 🏗 System Architecture

### Components

```
┌─────────────────────────────────────────────┐
│          FastAPI Server (Port 8000)         │
│  - Task Management REST API                 │
│  - Web Dashboard (Frontend)                 │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────┐
        │                     │          │
   ┌────▼─────┐    ┌─────────▼────┐   ┌─▼──────────┐
   │ Browser  │    │  Reasoning   │   │   OCR &    │
   │ Layer    │    │  Engine      │   │ Document   │
   │Playwright│    │ (Fara-7B)    │   │  Pipeline  │
   └────┬─────┘    └──────┬──────┘    └────┬───────┘
        │                 │                 │
   ┌────▼─────────────────▼─────────────────▼────┐
   │      Agentic Orchestrator                    │
   │  - Reason → Act → Observe → Update Loop     │
   │  - State Management                         │
   │  - Self-Correction Logic                    │
   └────┬─────────────────────────────────────────┘
        │
   ┌────▼─────────────────────────────┐
   │  System State & Logging           │
   │  - JSON Audit Logs                │
   │  - Downloaded Files               │
   │  - OCR Cache                      │
   │  - Task Results                   │
   └───────────────────────────────────┘
```

### Key Classes

- **`BrowserController`** - Playwright automation (click, fill, download, screenshot)
- **`FaraReasoningEngine`** - Fara-7B integration via Ollama
- **`OCRProcessor`** - Tesseract OCR with caching
- **`DocumentPipeline`** - End-to-end document processing
- **`AutomationOrchestrator`** - Main agentic loop
- **`FastAPI Server`** - REST API and task management

---

## 💡 How It Works

### Agentic Loop (Per Iteration)

1. **Observe**: Get current page HTML, title, URL
   ```json
   {
     "title": "Login Page",
     "url": "https://example.com/login",
     "html": "..."
   }
   ```

2. **Reason**: Fara-7B analyzes state and generates actions
   ```json
   [
     {"action": "fill", "selector": "#username", "value": "user@example.com", "reason": "Fill username field"},
     {"action": "fill", "selector": "#password", "value": "***", "reason": "Fill password field"},
     {"action": "click", "selector": "#login-btn", "reason": "Submit login form"}
   ]
   ```

3. **Act**: Execute actions via Playwright
   ```json
   {
     "action": "fill",
     "selector": "#username",
     "status": "success",
     "timestamp": "2025-12-06T10:30:05Z"
   }
   ```

4. **Update**: Log results, check for downloads, process OCR
   - Detected new file: `invoice_123.pdf`
   - Running OCR...
   - Extracted 2500 characters
   - Confidence: 0.94

5. **Loop** until objective complete

### Self-Correction

If selector fails:
```
❌ Failed to click #login-btn
  → Fara-7B analyzes HTML
  → Suggests: ["button[type='submit']", ".btn-primary", "#submit-form"]
  → Retries with corrected selector
  → Success! ✓
```

### Document Processing

```
Downloaded: invoice.pdf
  ↓
OCR Extraction (Tesseract)
  ↓
Text Cleaning (regex normalization)
  ↓
Classification (Fara-7B: "invoice")
  ↓
Field Extraction (JSON schema):
  {
    "vendor_name": "Acme Corp",
    "invoice_number": "INV-2025-001",
    "amount": "1500.00",
    "date": "2025-12-06"
  }
```

---

## 📡 API Reference

### Task Management

#### Create Task
```bash
POST /tasks
Content-Type: application/json

{
  "objective": "Login and download documents",
  "params": {"wait_for_download": true}
}

Response:
{
  "task_id": "uuid-here",
  "status": "queued"
}
```

#### Get Task Status
```bash
GET /tasks/{task_id}

Response:
{
  "task_id": "uuid-here",
  "status": "running|completed|failed",
  "started_at": "...",
  "completed_at": "...",
  "num_actions": 15
}
```

#### Get Task Result
```bash
GET /tasks/{task_id}/result

Response:
{
  "task_id": "uuid-here",
  "status": "completed|failed",
  "result": {...},
  "extracted_data": {
    "invoice.pdf": {...}
  }
}
```

#### Get Audit Log
```bash
GET /tasks/{task_id}/audit

Response:
[
  {
    "timestamp": "...",
    "action_type": "click",
    "action_data": {...},
    "status": "success|failed"
  },
  ...
]
```

#### List All Tasks
```bash
GET /tasks

Response:
[{task1}, {task2}, ...]
```

### Files

#### List Downloads
```bash
GET /downloads

Response:
[
  {
    "name": "invoice.pdf",
    "size": 125000,
    "created": 1733471400
  }
]
```

#### Download File
```bash
GET /downloads/{filename}
```

### System

#### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "service": "AI Document Automation Engine",
  "model": "Fara-7B (via Ollama)"
}
```

#### System Config
```bash
GET /system/config

Response:
{
  "ollama_url": "http://localhost:11434",
  "model": "fara-7b",
  "browser_headless": true,
  "max_retries": 3
}
```

#### System Logs
```bash
GET /system/logs?lines=50
```

---

## 📝 Configuration

### `.env` File

```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=fara-7b

# Target Website
TARGET_WEBSITE_URL=https://example.com
TARGET_USERNAME=user@example.com
TARGET_PASSWORD=secure_password

# Browser
BROWSER_HEADLESS=True           # False for debugging
BROWSER_TIMEOUT=30000           # ms
BROWSER_VIEWPORT_WIDTH=1280
BROWSER_VIEWPORT_HEIGHT=720

# System
DOWNLOAD_DIR=./downloads
CACHE_DIR=./cache
LOG_DIR=./logs
MAX_RETRIES=3                   # Retry failed actions
INFERENCE_TIMEOUT=120           # seconds

# Tesseract
TESSERACT_PATH=/usr/local/bin/tesseract

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False
```

---

## 📊 Logging & Audit

All actions are logged in JSON format for compliance and debugging.

### Logs Location
```
logs/
├── reasoning_engine.log      # Fara-7B decisions
├── browser_controller.log    # UI actions
├── ocr_processor.log         # OCR operations
├── agent_orchestrator.log    # Main loop
├── api_server.log            # API events
├── audit_<task_id>.json      # Per-task detailed audit
└── ...
```

### Example Audit Log
```json
[
  {
    "timestamp": "2025-12-06T10:30:05Z",
    "action_type": "goto",
    "action_data": {
      "action": "goto",
      "url": "https://example.com"
    },
    "status": "success"
  },
  {
    "timestamp": "2025-12-06T10:30:10Z",
    "event_type": "reasoning",
    "input_context": "Login form with username/password fields",
    "fara_decision": [
      {"action": "fill", "selector": "#username", ...}
    ],
    "confidence": 0.92
  },
  {
    "timestamp": "2025-12-06T10:30:20Z",
    "event_type": "document_extracted",
    "filename": "invoice.pdf",
    "doc_type": "invoice",
    "fields": {
      "vendor_name": "Acme Corp",
      "amount": "1500.00"
    },
    "confidence": 0.88
  }
]
```

---

## 🔧 Debugging

### Enable Debug Mode
```bash
# In .env
API_DEBUG=True

# In code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Logs in Real-time
```bash
# Terminal 1: Watch logs
tail -f logs/agent_orchestrator.log | jq '.' 2>/dev/null || cat -

# Terminal 2: Watch browser
# Set BROWSER_HEADLESS=False to see browser window
```

### Test Individual Components

```python
# Test OCR
from src.ocr.processor import OCRProcessor
ocr = OCRProcessor()
result = ocr.extract_text_from_image("./downloads/test.png")
print(result)

# Test Fara-7B
import asyncio
from src.reasoning.engine import FaraReasoningEngine
engine = FaraReasoningEngine()
result = asyncio.run(engine.analyze_page_state({
    "url": "https://example.com",
    "html": "<html>...</html>",
    "title": "Example"
}))
print(result)
```

---

## 🚀 Advanced Usage

### Custom Extraction Schema
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Extract invoice data",
    "params": {
      "extraction_schema": {
        "vendor": "Company/vendor name",
        "po_number": "Purchase order number",
        "total_amount": "Total invoice amount in currency"
      }
    }
  }'
```

### Headless Debugging
```bash
# In .env
BROWSER_HEADLESS=False
API_DEBUG=True

# Now you'll see:
# - Browser window (Chromium)
# - Detailed console logs
# - Screenshots saved per action
```

### Custom Workflow Steps

Extend `AutomationOrchestrator._agentic_loop()` to add:
- Email notifications
- Database updates
- Webhook callbacks
- Custom validation

---

## 🎯 Example Workflows

### Workflow 1: Invoice Download & Extraction

```json
{
  "objective": "Login to accounting.example.com, navigate to invoices, download latest invoice PDF, extract vendor name, invoice number, and total amount"
}
```

**Automated steps:**
1. ✓ Navigate to login page
2. ✓ Fill username/password
3. ✓ Submit login form
4. ✓ Navigate to Invoices section
5. ✓ Click download button
6. ✓ Wait for PDF download
7. ✓ Run OCR on PDF
8. ✓ Extract structured data
9. ✓ Save results as JSON

### Workflow 2: Multi-page Form Submission

```json
{
  "objective": "Fill and submit 5-step registration form with personal details, address, and preferences"
}
```

### Workflow 3: Data Comparison

```json
{
  "objective": "Download files from 3 different pages, compare extracted data, flag discrepancies"
}
```

---

## 📋 Troubleshooting

### Issue: "Ollama not responding"
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Ensure Fara-7B is pulled
ollama pull fara-7b
```

### Issue: "Tesseract not found"
```bash
# Find tesseract path
which tesseract
# Output: /usr/local/bin/tesseract

# Update .env
TESSERACT_PATH=/usr/local/bin/tesseract
```

### Issue: "Playwright browser not found"
```bash
# Install browsers
playwright install chromium

# Or reinstall
pip install --upgrade playwright
playwright install
```

### Issue: "Slow inference"
```bash
# Check Fara-7B context:
# Default: 4096 tokens
# For faster inference, reduce:
# FARA_TEMPERATURE=0.3  (more deterministic)
# FARA_TOP_K=20         (less sampling)
```

### Issue: "Downloaded file not found"
```bash
# Check download directory
ls -la ./downloads/

# Verify DOWNLOAD_DIR in .env
# Ensure browser can save files
```

---

## 📚 Documentation

- **Architecture**: See `docs/architecture.md`
- **API Spec**: See `docs/api.md`
- **Examples**: See `examples/`
- **Development**: See `DEVELOPMENT.md`

---

## 🔐 Security Notes

⚠️ **For Production Use:**
- Never commit `.env` with credentials
- Use secret management (Vault, AWS Secrets Manager)
- Encrypt credentials at rest
- Run in isolated network
- Monitor audit logs for anomalies
- Implement rate limiting on API
- Use HTTPS for production

---

## 📄 License

MIT License - See LICENSE file

---

## 👥 Support

Issues? Questions?
1. Check logs: `logs/`
2. Review audit trail: `logs/audit_<task_id>.json`
3. Enable debug mode and retry
4. Check `.env` configuration

---

**Built with ❤️ using Fara-7B, Ollama, Playwright, and Tesseract**
