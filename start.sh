#!/bin/bash
# Start script for Quest - AI Document Automation Engine

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🤖 AI Document Automation Engine${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Running setup...${NC}"
    bash setup.sh
fi

# Activate venv
source venv/bin/activate

echo -e "${BLUE}📋 Pre-flight checks:${NC}"
echo ""

# Check Python
python_version=$(python --version 2>&1)
echo -e "  ${GREEN}✓${NC} Python: $python_version"

# Check dependencies
echo -n "  ${GREEN}✓${NC} Dependencies: "
pip list | grep -q "playwright" && echo -n "Playwright " && true
pip list | grep -q "fastapi" && echo -n "FastAPI " && true
pip list | grep -q "pytesseract" && echo "Tesseract" && true

# Check Ollama
echo -n "  "
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Ollama: Running"
    
    if curl -s http://localhost:11434/api/tags | grep -q "fara-7b"; then
        echo -e "  ${GREEN}✓${NC} Fara-7B: Loaded"
    else
        echo -e "  ${YELLOW}⚠️  Fara-7B: Not found${NC}"
        echo -e "     ${YELLOW}Run: ollama pull fara-7b${NC}"
    fi
else
    echo -e "${RED}✗${NC} Ollama: Not running"
    echo -e "  ${YELLOW}Start with: ollama serve${NC}"
    exit 1
fi

# Check .env
echo -n "  "
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} Config: .env found"
else
    echo -e "${YELLOW}⚠️  .env: Not found${NC}"
    cp .env.example .env
    echo -e "  ${YELLOW}Created from template. Please update settings.${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Starting server...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Show connection info
echo -e "${GREEN}📡 Connection Info:${NC}"
echo -e "  API Server:   ${BLUE}http://localhost:8000${NC}"
echo -e "  Dashboard:    ${BLUE}http://localhost:8000/frontend/${NC}"
echo -e "  Health Check: ${BLUE}http://localhost:8000/health${NC}"
echo ""

echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start server
python main.py
