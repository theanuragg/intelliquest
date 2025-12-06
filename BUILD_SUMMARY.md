# 🎉 Quest - AI Document Automation Engine

**Complete autonomous document automation system built with Fara-7B, Ollama, Playwright, and Tesseract**

---

## ✅ What's Been Built

### Core System Components

1. **Browser Automation Layer** (`src/browser/controller.py`)
   - Playwright-based browser control
   - Actions: click, fill, goto, download, scroll, screenshot, wait
   - Full HTML snapshot after each action
   - Error logging and state tracking

2. **Fara-7B Reasoning Engine** (`src/reasoning/engine.py`)
   - Ollama integration with smart prompt engineering
   - Browser action generation from objectives
   - Document classification and information extraction
   - Self-correction for failed selectors
   - Workflow decision-making

3. **OCR & Document Pipeline** (`src/ocr/`)
   - Tesseract OCR integration (PDF, images)
   - Smart OCR error correction and text normalization
   - Result caching for efficiency
   - Metadata tracking and storage

4. **Agentic Orchestrator** (`src/agent/orchestrator.py`)
   - Main reason → act → observe → update loop
   - Automatic task execution in background
   - State management and error handling
   - Self-healing with Fara-7B assistance
   - Document detection and processing

5. **FastAPI Server** (`src/api/server.py`)
   - REST API for task management
   - Real-time status tracking
   - File management endpoints
   - System monitoring and logs
   - Health checks

6. **Web Dashboard** (`frontend/index.html`)
   - Modern, responsive UI
   - Real-time task monitoring
   - File downloads management
   - Task details and audit log viewer
   - Task creation with parameters

7. **Comprehensive Logging** (`src/utils/logger.py`)
   - JSON-formatted audit trails
   - Deep action logging
   - Document extraction tracking
   - Workflow decision recording
   - Per-task audit logs

### Supporting Infrastructure

- **Configuration System** (`src/config.py`) - Centralized settings via environment variables
- **Setup & Start Scripts** - Automated setup and convenient startup
- **Example Scripts** - Practical examples for common workflows
- **Documentation** - README, Quick Start, and inline code documentation

---

## 📁 Project Structure

```
quest/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── browser/
│   │   ├── __init__.py
│   │   └── controller.py         # Playwright automation
│   ├── reasoning/
│   │   ├── __init__.py
│   │   └── engine.py             # Fara-7B reasoning
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── processor.py          # Tesseract OCR
│   │   └── pipeline.py           # Document processing
│   ├── agent/
│   │   ├── __init__.py
│   │   └── orchestrator.py       # Main agentic loop
│   ├── api/
│   │   ├── __init__.py
│   │   └── server.py             # FastAPI server
│   └── utils/
│       ├── __init__.py
│       └── logger.py             # Logging system
├── frontend/
│   └── index.html                # Web dashboard
├── examples/
│   ├── example_basic.py
│   ├── example_invoice.py
│   └── api_client.py
├── logs/                         # Generated: audit trails
├── downloads/                    # Generated: downloaded files
├── cache/                        # Generated: OCR cache
├── main.py                       # Entry point
├── setup.sh                      # Setup automation
├── start.sh                      # Start server
├── requirements.txt              # Python dependencies
├── .env.example                  # Configuration template
├── .gitignore
├── README.md                     # Full documentation
└── QUICK_START.md               # Quick start guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
```bash
# Check all prerequisites are installed
ollama serve                # Terminal 1: Start Ollama + Fara-7B
cd /Users/anurag/coding/projects/quest
bash setup.sh              # Sets up venv, dependencies, config
```

### 2. Start Server
```bash
bash start.sh              # Terminal 2: Starts API server on :8000
```

### 3. Open Dashboard
```
http://localhost:8000/frontend/
```

### 4. Create First Task
- Enter objective: "Navigate to https://example.com and take a screenshot"
- Click "Create & Execute Task"
- Watch automation in real-time!

---

## 🎯 Key Features in Action

### Autonomous Task Execution
```json
Task: "Download invoice and extract vendor name and total"

Automated Actions:
1. Navigate to accounting.example.com
2. Fill login form
3. Submit login
4. Click "Invoices" menu
5. Find and click download button
6. Wait for PDF download
7. Run OCR extraction
8. Parse structured data
9. Save results as JSON
```

### Self-Correction
```
Action: Click #submit-button
Status: Failed - selector not found

Fara-7B Reasoning:
- Analyzed HTML
- Found: button[type='submit'].btn-primary
- Retried with corrected selector
- Success! ✓
```

### Document Intelligence
```
Downloaded: invoice.pdf

Processing:
1. OCR Extraction (Tesseract)
2. Text Cleaning (regex normalization)
3. Classification (Fara-7B: "invoice")
4. Field Extraction:
   {
     "vendor": "Acme Corp",
     "invoice_no": "INV-2025-001",
     "amount": "1500.00"
   }
```

---

## 💻 API Endpoints

### Task Management
```bash
# Create task
POST /tasks
{
  "objective": "...",
  "params": {...}
}

# Get status
GET /tasks/{task_id}

# Get result
GET /tasks/{task_id}/result

# Get audit log
GET /tasks/{task_id}/audit

# List all tasks
GET /tasks
```

### File Management
```bash
# List downloads
GET /downloads

# Download file
GET /downloads/{filename}
```

### System
```bash
# Health check
GET /health

# Configuration
GET /system/config

# Logs
GET /system/logs?lines=50
```

---

## 🔌 Integration Points

### Extend Reasoning
Edit `src/reasoning/engine.py`:
- Custom prompts for specific domains
- New classification types
- Specialized extraction schemas

### Add Workflow Steps
Edit `src/agent/orchestrator.py`:
- Database updates after extraction
- Email notifications
- Webhook callbacks
- Custom validation logic

### Custom Browser Actions
Edit `src/browser/controller.py`:
- Additional action types
- Custom event handling
- Plugin architecture

---

## 📊 Logging & Audit

### Audit Trail Example
```json
[
  {
    "timestamp": "2025-12-06T10:30:05Z",
    "action_type": "goto",
    "action_data": {"url": "https://example.com"},
    "status": "success"
  },
  {
    "timestamp": "2025-12-06T10:30:15Z",
    "event_type": "document_extracted",
    "filename": "invoice.pdf",
    "doc_type": "invoice",
    "confidence": 0.92
  }
]
```

### Log Files
- `logs/browser_controller.log` - Browser actions
- `logs/reasoning_engine.log` - AI decisions
- `logs/ocr_processor.log` - OCR operations
- `logs/agent_orchestrator.log` - Main loop
- `logs/audit_{task_id}.json` - Per-task detailed audit

---

## 🔧 Configuration

All settings in `.env`:
```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=fara-7b

# Website credentials
TARGET_WEBSITE_URL=https://example.com
TARGET_USERNAME=user@example.com
TARGET_PASSWORD=password

# System settings
MAX_RETRIES=3
INFERENCE_TIMEOUT=120
BROWSER_HEADLESS=True

# Paths
DOWNLOAD_DIR=./downloads
CACHE_DIR=./cache
LOG_DIR=./logs
```

---

## 🚦 Inference Parameters

Fara-7B is configured for optimal performance:
```python
FARA_CONTEXT_WINDOW = 4096      # Token limit
FARA_TEMPERATURE = 0.7          # Creativity (0.1-1.0)
FARA_TOP_P = 0.9                # Nucleus sampling
FARA_TOP_K = 40                 # Top-K sampling
FARA_REPEAT_PENALTY = 1.1       # Avoid repetition
```

Adjust in `src/config.py` for your needs:
- **Faster**: Lower temperature, reduce context window
- **Smarter**: Increase temperature, higher context
- **More creative**: Higher temperature
- **More deterministic**: Lower temperature

---

## 🎓 Learning Resources

### Understanding the System
1. Read `README.md` - Full documentation
2. Read `QUICK_START.md` - Quick reference
3. Review `src/config.py` - See all settings
4. Check `src/agent/orchestrator.py` - See main loop

### Running Examples
```bash
# Basic: Navigate and screenshot
python examples/example_basic.py

# Invoice workflow
python examples/example_invoice.py

# API client
python examples/api_client.py
```

### Debugging
```bash
# Enable headless mode off to see browser
BROWSER_HEADLESS=False

# Enable debug logging
API_DEBUG=True

# Watch logs in real-time
tail -f logs/agent_orchestrator.log | jq '.'
```

---

## 🔐 Security Considerations

✓ Credentials stored in `.env` (excluded from git)
✓ All API communication logged
✓ Audit trails for compliance
✓ Local-only operation (no cloud)

⚠️ Production recommendations:
- Use secrets manager for credentials
- Enable HTTPS on API
- Implement rate limiting
- Monitor audit logs
- Regular backups

---

## 🐛 Troubleshooting

### "Ollama not responding"
```bash
curl http://localhost:11434/api/tags
ollama serve  # If not running
ollama pull fara-7b  # If model missing
```

### "Tesseract not found"
```bash
which tesseract  # Find path
# Update TESSERACT_PATH in .env
```

### "Browser not downloading"
```bash
# Check directory
ls -la ./downloads/

# Enable debug mode
BROWSER_HEADLESS=False
```

### "Task too slow"
```bash
# Reduce inference overhead
FARA_TEMPERATURE=0.3  # More deterministic
FARA_TOP_K=20         # Faster sampling
INFERENCE_TIMEOUT=60  # Reduce timeout
```

---

## 🎯 Next Steps

1. **Run first task** - Use web dashboard to create task
2. **Create custom workflow** - Modify objective for your use case
3. **Add integrations** - Connect to your databases/APIs
4. **Deploy to production** - Follow security checklist
5. **Monitor continuously** - Check logs and audit trails

---

## 📦 What's Included

- ✓ Complete agentic system
- ✓ FastAPI server with REST API
- ✓ Modern web dashboard
- ✓ OCR pipeline with caching
- ✓ Comprehensive logging
- ✓ Example scripts
- ✓ Documentation
- ✓ Setup automation

## ⚡ What's NOT Included

- Database integration (you can add)
- Email notifications (you can add)
- Webhook callbacks (you can add)
- Advanced UI analytics (you can add)
- Kubernetes deployment (you can add)

---

## 📞 Support

**Issues?**
1. Check logs: `logs/`
2. Enable debug: `API_DEBUG=True`
3. Review examples: `examples/`
4. Read docs: `README.md`

**Want to extend?**
1. Edit config: `src/config.py`
2. Modify prompts: `src/reasoning/engine.py`
3. Add actions: `src/browser/controller.py`
4. Custom workflows: `src/agent/orchestrator.py`

---

## 🎉 You're All Set!

Your AI-powered document automation system is ready to go!

```bash
# 1. Start Ollama
ollama serve

# 2. Start Quest
bash start.sh

# 3. Open dashboard
http://localhost:8000/frontend/

# 4. Create your first task!
```

**Enjoy autonomous automation! 🤖**

---

Built with ❤️ using:
- **Fara-7B** - Advanced reasoning model
- **Ollama** - Local inference engine
- **Playwright** - Browser automation
- **Tesseract** - OCR technology
- **FastAPI** - Modern web framework
- **Python** - Programming language
