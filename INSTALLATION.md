# Complete Installation Guide

Follow these steps to get Quest running on your system.

---

## ⏱ Time: ~15 minutes

---

## Prerequisites

### 1. Ollama + Fara-7B

**macOS:**
```bash
# Install Ollama
brew install ollama

# Pull Fara-7B model
ollama pull fara-7b

# Verify installation
ollama list | grep fara-7b
```

**Linux (Ubuntu/Debian):**
```bash
# Download from https://ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull fara-7b
```

**Windows:**
- Download installer from https://ollama.ai
- Run installer
- Open PowerShell and run:
  ```powershell
  ollama pull fara-7b
  ```

### 2. Python 3.9+

```bash
python --version
# Should show: Python 3.9.0 or higher

# If not installed
brew install python@3.11  # macOS
sudo apt install python3.11  # Linux
# Windows: https://www.python.org/downloads/
```

### 3. Tesseract OCR

**macOS:**
```bash
brew install tesseract

# Verify
tesseract --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr

# Verify
tesseract --version
```

**Windows:**
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (keep default path: `C:\Program Files\Tesseract-OCR`)
3. Verify:
   ```powershell
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```

### 4. Git (Optional, for version control)

```bash
git --version
# If not installed
brew install git  # macOS
sudo apt install git  # Linux
```

---

## Installation Steps

### Step 1: Clone/Navigate to Project

```bash
cd /Users/anurag/coding/projects/quest
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# On Windows:
# venv\Scripts\activate.bat
```

**Expected output:**
```
(venv) $ 
```

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Optional: Install PDF support**
```bash
pip install pdf2image
```

### Step 4: Setup Configuration

```bash
# Copy template
cp .env.example .env

# Edit configuration
nano .env
# or: code .env
```

**Important fields to set:**
```
TARGET_WEBSITE_URL=https://your-target-website.com
TARGET_USERNAME=your-username
TARGET_PASSWORD=your-password
TESSERACT_PATH=/usr/local/bin/tesseract
```

**Find Tesseract path:**
```bash
which tesseract
# Output: /usr/local/bin/tesseract
# Use this path in TESSERACT_PATH=
```

### Step 5: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 6: Verify Installation

```bash
# Check all components
echo "1. Python:"
python --version

echo "2. Tesseract:"
tesseract --version

echo "3. Dependencies:"
pip list | grep -E "playwright|fastapi|pytesseract"

echo "4. Ollama:"
curl http://localhost:11434/api/tags 2>/dev/null | grep -q fara-7b && echo "✓ Fara-7B found" || echo "✗ Fara-7B not found - run: ollama pull fara-7b"
```

---

## Quick Start

### Terminal 1: Start Ollama
```bash
ollama serve
# Output: Listening on 127.0.0.1:11434
```

### Terminal 2: Start Quest
```bash
cd /Users/anurag/coding/projects/quest
source venv/bin/activate  # or: . venv/bin/activate
bash start.sh
```

**Expected output:**
```
🤖 AI Document Automation Engine
✓ Python: Python 3.11.0
✓ Dependencies: Playwright FastAPI Tesseract
✓ Ollama: Running
✓ Fara-7B: Loaded
✓ Config: .env found

🚀 Starting server...

📡 Connection Info:
  API Server:   http://localhost:8000
  Dashboard:    http://localhost:8000/frontend/
  Health Check: http://localhost:8000/health

Press Ctrl+C to stop the server
```

### Terminal 3: Open Dashboard
```bash
# Open in browser
open http://localhost:8000/frontend/

# Or manually
# Visit: http://localhost:8000/frontend/
```

---

## Troubleshooting Installation

### Issue: Python not found
```bash
# Check if Python 3.9+ is installed
python3 --version

# If not installed
brew install python@3.11  # macOS
sudo apt install python3.11  # Linux
```

### Issue: Tesseract not found
```bash
# Verify installation
which tesseract
tesseract --version

# If not installed
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Linux

# Update .env with correct path
nano .env
# Set: TESSERACT_PATH=/path/from/which
```

### Issue: pip command not found
```bash
# Make sure venv is activated
source venv/bin/activate

# Should show (venv) prompt
# If not, create new venv:
python3 -m venv venv
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Issue: Playwright install fails
```bash
# Try installing manually
playwright install chromium

# If that fails, update playwright
pip install --upgrade playwright
playwright install
```

### Issue: Ollama connection failed
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If fails, start Ollama
ollama serve

# Check if Fara-7B is installed
curl http://localhost:11434/api/tags | grep fara-7b

# If missing, pull it
ollama pull fara-7b
```

### Issue: Port 8000 already in use
```bash
# Find process using port
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>

# Or use different port in .env
API_PORT=8001
```

---

## Verification Checklist

Run this to verify everything is working:

```bash
#!/bin/bash

echo "✓ Checking Quest Installation"
echo ""

# 1. Python
echo "1. Python Version:"
python --version || echo "   ✗ Python not found"

# 2. Venv
echo "2. Virtual Environment:"
[ -d "venv" ] && echo "   ✓ venv directory exists" || echo "   ✗ venv not found"

# 3. Dependencies
echo "3. Key Dependencies:"
python -c "import playwright; print('   ✓ Playwright')" 2>/dev/null || echo "   ✗ Playwright"
python -c "import fastapi; print('   ✓ FastAPI')" 2>/dev/null || echo "   ✗ FastAPI"
python -c "import pytesseract; print('   ✓ Pytesseract')" 2>/dev/null || echo "   ✗ Pytesseract"

# 4. Tesseract
echo "4. Tesseract OCR:"
which tesseract > /dev/null && echo "   ✓ Tesseract installed at: $(which tesseract)" || echo "   ✗ Tesseract not found"

# 5. Ollama
echo "5. Ollama:"
curl -s http://localhost:11434/api/tags > /dev/null && echo "   ✓ Ollama running" || echo "   ✗ Ollama not running"

# 6. Fara-7B
echo "6. Fara-7B Model:"
curl -s http://localhost:11434/api/tags | grep -q fara-7b && echo "   ✓ Fara-7B available" || echo "   ✗ Fara-7B not found (run: ollama pull fara-7b)"

# 7. Config
echo "7. Configuration:"
[ -f ".env" ] && echo "   ✓ .env file exists" || echo "   ✗ .env not found (run: cp .env.example .env)"

# 8. Directories
echo "8. Directories:"
[ -d "logs" ] && echo "   ✓ logs directory" || echo "   ✗ logs missing"
[ -d "downloads" ] && echo "   ✓ downloads directory" || echo "   ✗ downloads missing"
[ -d "cache" ] && echo "   ✓ cache directory" || echo "   ✗ cache missing"

echo ""
echo "Installation verification complete!"
```

Save as `verify.sh` and run:
```bash
bash verify.sh
```

---

## Next Steps

1. ✓ Complete installation
2. → Start Ollama: `ollama serve`
3. → Start Quest: `bash start.sh`
4. → Open Dashboard: `http://localhost:8000/frontend/`
5. → Read QUICK_START.md for first task

---

## Getting Help

If installation fails:

1. **Check all prerequisites** - Run `bash verify.sh`
2. **Review logs** - Check `logs/` directory
3. **Check Ollama status** - `curl http://localhost:11434/api/tags`
4. **Review README.md** - Full documentation
5. **Check DEVELOPMENT.md** - For customization/debugging

---

**Installation complete!** 🎉

Now proceed to QUICK_START.md to create your first task.
