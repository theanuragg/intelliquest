#!/bin/bash
# Setup script for Quest - AI Document Automation Engine

set -e

echo "🚀 Setting up AI Document Automation Engine..."

# Check Python
echo "✓ Checking Python..."
python_version=$(python3 --version 2>&1)
echo "  $python_version"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -q -r requirements.txt

# Optional: Install pdf2image for PDF support
echo "📥 Installing optional PDF support..."
pip install -q pdf2image || echo "  (pdf2image optional - for PDF processing)"

# Check Tesseract
echo "✓ Checking Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    tesseract_version=$(tesseract --version 2>&1 | head -1)
    echo "  Found: $tesseract_version"
else
    echo "  ⚠️  Tesseract not found. Install with:"
    echo "      macOS: brew install tesseract"
    echo "      Ubuntu: sudo apt-get install tesseract-ocr"
    echo "      Then update TESSERACT_PATH in .env"
fi

# Check Playwright
echo "✓ Checking Playwright browsers..."
playwright install chromium > /dev/null 2>&1 || true

# Setup .env
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "  ⚠️  Please edit .env with your settings:"
    echo "      - TARGET_WEBSITE_URL"
    echo "      - TARGET_USERNAME"
    echo "      - TARGET_PASSWORD"
    echo "      - TESSERACT_PATH (if different)"
fi

# Check Ollama
echo "✓ Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  ✓ Ollama is running"
    
    # Check for Fara-7B
    if curl -s http://localhost:11434/api/tags | grep -q "fara-7b"; then
        echo "  ✓ Fara-7B model found"
    else
        echo "  ⚠️  Fara-7B not found. Pull it with:"
        echo "      ollama pull fara-7b"
    fi
else
    echo "  ⚠️  Ollama not running. Start it with:"
    echo "      ollama serve"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Verify .env configuration:"
echo "      nano .env"
echo ""
echo "   2. Start Ollama (if not running):"
echo "      ollama serve"
echo ""
echo "   3. Start the server:"
echo "      python main.py"
echo ""
echo "   4. Open dashboard:"
echo "      http://localhost:8000/frontend/"
echo ""
