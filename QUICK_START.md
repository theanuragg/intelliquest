# AI Document Automation Engine - Getting Started

## ⚡ Quick Start (5 minutes)

### 1. Prerequisites Checklist

- [ ] Ollama installed and running with Fara-7B
- [ ] Python 3.9+
- [ ] Tesseract OCR installed
- [ ] Terminal access

### 2. One-Command Setup

```bash
cd /Users/anurag/coding/projects/quest
bash setup.sh
```

This will:
- ✓ Create Python virtual environment
- ✓ Install all dependencies
- ✓ Check Tesseract installation
- ✓ Setup Playwright browsers
- ✓ Create `.env` file from template

### 3. Configure

Edit `.env` with your settings:
```bash
nano .env
```

Required settings:
```
TARGET_WEBSITE_URL=https://your-site.com
TARGET_USERNAME=your-username
TARGET_PASSWORD=your-password
TESSERACT_PATH=/usr/local/bin/tesseract  # Check with: which tesseract
```

### 4. Start Everything

**Terminal 1 - Start Ollama (if not running):**
```bash
ollama serve
```

**Terminal 2 - Start Quest Server:**
```bash
cd /Users/anurag/coding/projects/quest
bash start.sh
```

**Terminal 3 - Open Dashboard:**
```bash
# Your browser
http://localhost:8000/frontend/
```

## 🎯 First Task

1. Go to http://localhost:8000/frontend/
2. In **"Create Task"** box, enter:
   ```
   Navigate to https://example.com and take a screenshot
   ```
3. Click **"Create & Execute Task"**
4. Watch the browser automation in action!

## 📊 Monitoring

### Web Dashboard
- Real-time task monitoring
- Download file management
- View extracted data

### API Endpoints
```bash
# Check health
curl http://localhost:8000/health

# Get tasks
curl http://localhost:8000/tasks

# View specific task
curl http://localhost:8000/tasks/{task_id}

# Download results
curl http://localhost:8000/tasks/{task_id}/result

# Audit trail
curl http://localhost:8000/tasks/{task_id}/audit
```

### Logs
```bash
# Watch main logs
tail -f logs/agent_orchestrator.log

# Watch OCR
tail -f logs/ocr_processor.log

# Watch browser
tail -f logs/browser_controller.log

# View specific task audit
cat logs/audit_{task_id}.json | jq '.'
```

## 🔧 Troubleshooting

### Ollama not responding
```bash
# Check if running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull Fara-7B if missing
ollama pull fara-7b
```

### Tesseract not found
```bash
# Find path
which tesseract

# Update .env with correct path
nano .env
# TESSERACT_PATH=/path/from/which
```

### Browser not downloading files
```bash
# Check downloads directory exists
ls -la ./downloads/

# Enable debug mode in .env
BROWSER_HEADLESS=False
API_DEBUG=True

# Check browser window for permission dialogs
```

### Slow inference
- Reduce context: Edit `src/config.py` → `FARA_CONTEXT_WINDOW`
- Reduce temperature: Edit `src/config.py` → `FARA_TEMPERATURE`
- Check Ollama is not overloaded: `curl http://localhost:11434/api/tags`

## 📚 Advanced Usage

### Example Scripts

```bash
# Basic example
python examples/example_basic.py

# Invoice extraction example
python examples/example_invoice.py

# API client example
python examples/api_client.py
```

### Custom Workflows

Extend tasks in `src/agent/orchestrator.py`:
- Override `_agentic_loop()` for custom logic
- Add webhook callbacks
- Implement database persistence
- Add email notifications

### Using Headless: False for Debugging

```bash
# Edit .env
BROWSER_HEADLESS=False
API_DEBUG=True

# Run server
python main.py

# Now you'll see:
# - Live browser window (Chromium)
# - Detailed console logs
# - Pauses on errors for inspection
```

## 🚀 Production Checklist

- [ ] Use environment variables for credentials (not .env)
- [ ] Enable HTTPS for API
- [ ] Implement rate limiting
- [ ] Setup monitoring/alerts
- [ ] Configure log rotation
- [ ] Use secrets manager for sensitive data
- [ ] Setup audit log archival
- [ ] Implement backup strategy

## 📖 Full Documentation

- Full README: `README.md`
- Architecture details: `docs/architecture.md` (TODO)
- API reference: `docs/api.md` (TODO)

## 🆘 Getting Help

1. **Check logs** - Most answers in `logs/`
2. **Review examples** - See `examples/` folder
3. **Enable debug mode** - Set `API_DEBUG=True`
4. **Check audit trail** - View `logs/audit_{task_id}.json`

## ✨ Next Steps

1. ✓ Complete setup
2. ✓ Run first task
3. → Create custom workflow for your use case
4. → Integrate with your existing systems
5. → Monitor in production

---

**Need to understand the architecture?** See `README.md` section "How It Works"

**Want to modify behavior?** Edit files in `src/` directory

**Running into issues?** Check "Troubleshooting" section above

---

**Happy automating! 🤖**
