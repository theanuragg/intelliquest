# 🎯 START HERE - Quest AI Document Automation

Welcome! This file will get you up and running in **5 minutes**.

---

## What is Quest?

An AI-powered system that:
- **Autonomously logs into websites**
- **Navigates complex UI** (clicks, fills, waits)
- **Downloads documents** (PDF, images)
- **Runs OCR** (extract text)
- **Extracts structured data** (JSON)
- **Self-corrects** when things fail
- **Logs everything** for audit/compliance

Powered by **Fara-7B**, **Ollama**, **Playwright**, and **Tesseract**.

Everything runs **locally**. No cloud. No API charges.

---

## 3-Step Quick Start

### Step 1: Prerequisites (1 min)

```bash
# Check these are installed:
python --version           # Python 3.9+
ollama list               # Ollama running, Fara-7B installed
which tesseract          # Tesseract OCR installed

# If Ollama not running:
ollama serve &
```

**Not installed?** See `INSTALLATION.md`

### Step 2: Setup (2 min)

```bash
cd /Users/anurag/coding/projects/quest
bash setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Setup configuration file

### Step 3: Start & Use (2 min)

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
cd /Users/anurag/coding/projects/quest
bash start.sh
```

**Terminal 3 (your browser):**
```
http://localhost:8000/frontend/
```

---

## First Task (Under 1 minute)

1. Open http://localhost:8000/frontend/
2. In the **"Create Task"** box, enter:
   ```
   Navigate to https://example.com and take a screenshot
   ```
3. Click **"Create & Execute Task"**
4. Watch the browser tab do it automatically!
5. Click the task ID to see results and audit log

---

## 📚 Documentation

Pick what you need:

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **QUICK_START.md** | Commands & monitoring | 5 min |
| **INSTALLATION.md** | Detailed setup | 15 min |
| **README.md** | Full reference | 30 min |
| **DEVELOPMENT.md** | How to customize | 20 min |

---

## �� Common Tasks

### Create Invoice Automation
```json
{
  "objective": "Login to accounting.example.com, navigate to invoices, download latest PDF, extract vendor name and amount"
}
```

### Extract Multiple Documents
```json
{
  "objective": "Process 3 documents in folder: classify type, extract key fields, save as JSON"
}
```

### Form Submission
```json
{
  "objective": "Fill and submit registration form with auto-generated user data"
}
```

---

## 🔌 Using the API

Instead of web UI, use API directly:

```bash
# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Navigate to example.com"
  }'

# Get status
curl http://localhost:8000/tasks/{task_id}

# Get results
curl http://localhost:8000/tasks/{task_id}/result

# Get audit log
curl http://localhost:8000/tasks/{task_id}/audit
```

---

## 📊 Real-time Monitoring

**Web Dashboard:**
- Visit http://localhost:8000/frontend/
- Real-time task status
- Download files
- View audit logs

**Command Line:**
```bash
# Watch logs
tail -f logs/agent_orchestrator.log

# Monitor OCR
tail -f logs/ocr_processor.log

# View browser actions
tail -f logs/browser_controller.log
```

---

## 🆘 Help & Troubleshooting

**Dashboard won't load?**
```bash
# Check server is running
curl http://localhost:8000/health

# Check Ollama
curl http://localhost:11434/api/tags
```

**Tesseract not found?**
```bash
which tesseract
# Update TESSERACT_PATH in .env
nano .env
```

**Task stuck?**
```bash
# Check logs
tail -f logs/audit_{task_id}.json | jq '.'

# Restart server
# Press Ctrl+C in Terminal 2
bash start.sh
```

See **QUICK_START.md** or **INSTALLATION.md** for more help.

---

## 💡 Tips

1. **Use web dashboard** for first tasks (visual feedback)
2. **Use API** for automation (integrations)
3. **Check logs** when tasks fail (diagnosis)
4. **Read examples** for patterns (examples/ folder)
5. **Customize prompts** for your domain (DEVELOPMENT.md)

---

## 🚀 Next Steps

1. ✅ Create your first task (above)
2. → Explore the dashboard
3. → Try an example (examples/ folder)
4. → Customize for your use case
5. → Add integrations (database, email, etc.)

---

## 📁 Project Structure

```
quest/
├── src/                    # Source code (don't edit, understand it)
├── frontend/index.html     # Web dashboard
├── examples/               # Example scripts
├── logs/                   # Audit trails (generated)
├── downloads/              # Downloaded files (generated)
├── .env                    # Your configuration
├── main.py                 # Start with: python main.py
├── README.md               # Full reference
├── QUICK_START.md          # Commands & troubleshooting
├── INSTALLATION.md         # Setup guide
└── DEVELOPMENT.md          # Customization guide
```

---

## 🔧 Configuration

Edit `.env`:
```bash
nano .env
```

Key settings:
- `TARGET_WEBSITE_URL` - Your website
- `TARGET_USERNAME` - Login username
- `TARGET_PASSWORD` - Login password
- `TESSERACT_PATH` - Path to tesseract (find with: which tesseract)
- `BROWSER_HEADLESS=False` - See browser (for debugging)

---

## 🎓 Learning Path

**Complete beginner:**
1. Read this file (START_HERE.md)
2. Run Step 1-3 above
3. Create first task
4. Explore dashboard

**Want to customize:**
1. Read DEVELOPMENT.md
2. Look at examples/
3. Modify src/ files
4. Test with dashboard

**Want to integrate:**
1. Read API reference in README.md
2. Look at examples/api_client.py
3. Write your integration
4. Test with your system

---

## ⚡ Pro Tips

**Faster inference:**
```bash
# Edit .env
FARA_TEMPERATURE=0.3  # Lower = more deterministic
FARA_TOP_K=20        # Lower = faster
```

**Debug tasks:**
```bash
# Edit .env
BROWSER_HEADLESS=False    # See browser window
API_DEBUG=True            # Verbose logs
```

**Monitor in production:**
```bash
# API endpoint shows system stats
curl http://localhost:8000/system/config
curl http://localhost:8000/system/logs?lines=100
```

---

## ✨ You're Ready!

Everything is set up. Pick a task and let Quest do the work.

```
1. Dashboard → http://localhost:8000/frontend/
2. API → POST http://localhost:8000/tasks
3. CLI → python examples/api_client.py
```

**Questions?** Check:
- QUICK_START.md - Common issues
- README.md - Full docs
- DEVELOPMENT.md - Customization
- examples/ - Code examples

---

## 📞 Quick Reference

```bash
# Start everything
ollama serve &
cd /Users/anurag/coding/projects/quest
bash start.sh

# View logs
tail -f logs/agent_orchestrator.log | jq '.'

# Test API
curl http://localhost:8000/health

# Run example
python examples/api_client.py
```

---

**Happy automating! 🤖**

Start with the dashboard: http://localhost:8000/frontend/
