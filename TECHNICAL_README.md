# 🔬 IntelliQuest - Technical Documentation

**Version:** 1.0.0  
**Last Updated:** December 2025

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [What is IntelliQuest](#what-is-intelliquest)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Core Components](#core-components)
6. [Data Flow & Processing](#data-flow--processing)
7. [API Specification](#api-specification)
8. [Configuration Management](#configuration-management)
9. [Security Architecture](#security-architecture)
10. [Development Guide](#development-guide)
11. [Deployment Strategies](#deployment-strategies)
12. [Performance Optimization](#performance-optimization)
13. [Testing & Debugging](#testing--debugging)
14. [Extension Points](#extension-points)
15. [Troubleshooting Guide](#troubleshooting-guide)

---

## Project Overview

### What is IntelliQuest?

IntelliQuest is an **autonomous AI-powered document automation engine** that combines browser automation, optical character recognition (OCR), and advanced reasoning capabilities to create an intelligent agent system. It can autonomously interact with web applications, extract information from documents, and process data without human intervention.

**Key Capabilities:**
- 🤖 **Autonomous Web Navigation** - Intelligently navigates websites using AI-driven decision making
- 📄 **Document Processing** - Extracts text from PDFs, images (JPG, PNG, TIFF) using OCR
- 🧠 **AI Reasoning** - Uses Fara-7B LLM for contextual understanding and action planning
- 🔄 **Self-Correction** - Automatically recovers from failures and adapts strategies
- 📊 **Structured Data Extraction** - Converts unstructured document text to JSON schemas
- 🔍 **Comprehensive Audit Logging** - Tracks every action for compliance and debugging
- 🌐 **REST API** - Full-featured API for integration with other systems
- 💻 **Web Dashboard** - Modern UI for monitoring and control
- 🔒 **100% Local Execution** - No cloud dependencies, all processing happens locally

### Use Cases

1. **Invoice Processing Automation**
   - Login to vendor portals
   - Download invoices automatically
   - Extract vendor names, amounts, PO numbers
   - Export to JSON for ERP integration

2. **Document Classification & Archival**
   - Process documents from multiple sources
   - Classify by type (invoice, receipt, contract, etc.)
   - Extract metadata
   - Archive with proper tagging

3. **Form Submission Automation**
   - Fill multi-step forms intelligently
   - Handle dynamic form fields
   - Submit and verify completion
   - Capture confirmation data

4. **Data Extraction & Comparison**
   - Download documents from multiple sources
   - Extract and normalize data
   - Compare across documents
   - Flag discrepancies for review

5. **Compliance & Audit Trail**
   - Automated document collection
   - Complete action logging
   - Time-stamped audit trails
   - Screenshot evidence capture

---

## Technology Stack

### Core Technologies

#### 1. **Python 3.9+**
- **Role:** Primary programming language
- **Why:** Excellent async support, rich ecosystem for AI/ML, strong library support
- **Key Libraries:**
  - `asyncio` - Asynchronous I/O operations
  - `pathlib` - Modern file system paths
  - `typing` - Type hints for better code quality

#### 2. **Fara-7B (via Ollama)**
- **Role:** Large Language Model for reasoning and decision-making
- **Why:** Locally runnable, no API costs, privacy-preserving
- **Capabilities:**
  - Natural language understanding
  - HTML/DOM analysis
  - Action planning
  - Document classification
  - Information extraction
  - Self-correction logic

#### 3. **Playwright**
- **Version:** 1.40.0
- **Role:** Browser automation framework
- **Why:** Modern, reliable, supports multiple browsers, excellent async API
- **Features Used:**
  - Page navigation and interaction
  - Element selection (CSS, XPath)
  - File download handling
  - Screenshot capture
  - Network monitoring
  - Context isolation

#### 4. **Tesseract OCR**
- **Role:** Optical Character Recognition engine
- **Why:** Open-source, highly accurate, multi-language support
- **Integration:** Via `pytesseract` Python wrapper
- **Supports:** Images, PDFs (via pdf2image), TIFF

#### 5. **FastAPI**
- **Version:** 0.109.0
- **Role:** Web framework for REST API
- **Why:** Modern, fast, automatic OpenAPI documentation, async support
- **Features:**
  - RESTful endpoint design
  - Automatic request validation
  - Background task execution
  - Static file serving
  - CORS support

#### 6. **Uvicorn**
- **Version:** 0.27.0
- **Role:** ASGI server
- **Why:** High performance, production-ready, WebSocket support

### Supporting Technologies

- **Pydantic** (2.5.2) - Data validation and settings management
- **python-dotenv** (1.0.0) - Environment variable management
- **Pillow** (10.1.0) - Image processing
- **requests** (2.31.0) - HTTP client for Ollama API
- **httpx** (0.25.2) - Async HTTP client
- **aiofiles** (23.2.1) - Async file I/O
- **python-json-logger** (2.0.7) - Structured logging
- **pdf2image** - PDF to image conversion

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  ┌──────────────────┐              ┌────────────────────┐       │
│  │  Web Dashboard   │              │   API Clients      │       │
│  │  (HTML/JS/CSS)   │              │   (curl, Python)   │       │
│  └────────┬─────────┘              └──────────┬─────────┘       │
└───────────┼────────────────────────────────────┼─────────────────┘
            │                                    │
            └────────────────┬───────────────────┘
                             │ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Endpoints: /tasks, /downloads, /system, /health         │   │
│  │  - Task Management (CRUD operations)                     │   │
│  │  - File Management (download, list)                      │   │
│  │  - System Monitoring (logs, config, health)             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ Internal Python API
┌─────────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           AutomationOrchestrator                          │   │
│  │  - Task lifecycle management                             │   │
│  │  - Agentic loop coordination                             │   │
│  │  - State management                                      │   │
│  │  - Audit logging                                         │   │
│  └──┬────────────────────┬─────────────────────┬────────────┘   │
└─────┼────────────────────┼─────────────────────┼────────────────┘
      │                    │                     │
      │                    │                     │
┌─────▼──────────┐  ┌──────▼─────────┐  ┌───────▼──────────┐
│   Browser      │  │   Reasoning    │  │   OCR &          │
│   Controller   │  │   Engine       │  │   Document       │
│                │  │                │  │   Pipeline       │
│  Playwright    │  │   Fara-7B      │  │   Tesseract      │
│  - Navigate    │  │  - Analyze     │  │  - Extract text  │
│  - Click       │  │  - Plan        │  │  - Clean text    │
│  - Fill        │  │  - Correct     │  │  - Classify      │
│  - Download    │  │  - Extract     │  │  - Structure     │
└─────┬──────────┘  └────────┬───────┘  └──────────┬───────┘
      │                      │                      │
      └──────────────────────┼──────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                     External Services                            │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────────┐     │
│  │   Ollama    │   │  Tesseract   │   │  Target Website  │     │
│  │   Service   │   │    OCR       │   │                  │     │
│  │ (Fara-7B)   │   │              │   │  (Web Apps)      │     │
│  └─────────────┘   └──────────────┘   └──────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                               │
│  ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌────────────┐    │
│  │   Logs    │  │ Downloads │  │  Cache   │  │   Config   │    │
│  │  (JSON)   │  │  (files)  │  │  (OCR)   │  │   (.env)   │    │
│  └───────────┘  └───────────┘  └──────────┘  └────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Architectural Patterns

#### 1. **Agentic Architecture**
- **Pattern:** Observe → Reason → Act → Update loop
- **Benefits:**
  - Autonomous decision-making
  - Self-correction capabilities
  - Adaptive behavior
  - Resilience to failures

#### 2. **Layered Architecture**
- **Presentation Layer:** Web UI + REST API
- **Business Logic Layer:** Orchestrator + Components
- **Data Layer:** File system storage
- **Benefits:**
  - Separation of concerns
  - Easy testing
  - Maintainability

#### 3. **Asynchronous Processing**
- **Pattern:** Async/await throughout the stack
- **Benefits:**
  - Non-blocking I/O
  - Better resource utilization
  - Scalability
  - Responsive API

#### 4. **Microkernel/Plugin Architecture**
- **Core:** Orchestrator + Base components
- **Extensions:** Custom processors, extractors, validators
- **Benefits:**
  - Extensibility
  - Customization
  - Modularity

---

## Core Components

### 1. AutomationOrchestrator

**File:** `src/agent/orchestrator.py`

**Purpose:** Central coordinator that manages the entire automation lifecycle.

**Key Responsibilities:**
- Task creation and lifecycle management
- Agentic loop execution (Reason → Act → Observe → Update)
- Component coordination (Browser, Reasoning, OCR)
- State management
- Audit logging
- Error handling and recovery

**Class: AutomationTask**
```python
class AutomationTask:
    task_id: str              # Unique identifier (UUID)
    objective: str            # Natural language task description
    params: Dict[str, Any]    # Optional parameters
    status: str               # pending|running|completed|failed
    started_at: datetime
    completed_at: datetime
    result: Dict              # Task execution result
    error: str                # Error message if failed
    completed_actions: List   # History of all actions
    extracted_data: Dict      # Data extracted from documents
```

**Main Methods:**
- `create_task(objective, params)` - Create new automation task
- `execute_task(task_id)` - Execute task through agentic loop
- `_agentic_loop(task)` - Main decision-action cycle
- `_check_and_process_downloads(task)` - Process downloaded files
- `get_task_status(task_id)` - Retrieve task status
- `get_task_audit_log(task_id)` - Get audit trail

**Agentic Loop Flow:**
```python
while iteration < max_iterations:
    # 1. Observe: Get current page state
    page_state = await self.browser.get_page_state()
    
    # 2. Reason: AI determines next actions
    reasoning_result = await self.reasoning_engine.generate_browser_actions(
        objective=task.objective,
        page_state=page_state,
        previous_actions=task.completed_actions
    )
    
    # 3. Act: Execute actions
    for action in actions:
        result = await self.browser.execute_action(action)
        # Handle failures with retries and self-correction
        if result['status'] == 'failed':
            corrected_action = await self.reasoning_engine.self_correct_selector(...)
    
    # 4. Update: Process results, check downloads
    await self._check_and_process_downloads(task)
```

---

### 2. FaraReasoningEngine

**File:** `src/reasoning/engine.py`

**Purpose:** AI reasoning layer using Fara-7B for intelligent decision-making.

**Key Responsibilities:**
- Analyze webpage state and HTML structure
- Generate browser automation actions
- Document classification
- Information extraction
- Selector self-correction
- Workflow decision-making

**Main Methods:**

1. **`analyze_page_state(page_state)`**
   - Analyzes current webpage
   - Identifies page type (login, form, dashboard, etc.)
   - Extracts key elements
   - Suggests next actions
   - Returns: Analysis + recommendations

2. **`generate_browser_actions(objective, page_state, previous_actions)`**
   - Core reasoning function
   - Takes objective + current state
   - Generates sequence of browser actions
   - Returns: JSON array of actions with selectors

3. **`extract_information(text, extraction_schema)`**
   - Structured data extraction
   - Takes raw text + schema definition
   - Returns: Extracted fields + confidence scores

4. **`classify_document(text)`**
   - Document type classification
   - Possible types: invoice, receipt, form, ID card, bank statement, contract
   - Returns: Document type + confidence + indicators

5. **`self_correct_selector(failed_selector, html, element_description)`**
   - Automatic error recovery
   - Analyzes HTML when selector fails
   - Suggests alternative selectors
   - Returns: Corrected selectors in priority order

6. **`determine_next_workflow_step(current_state, completed_actions, extracted_data)`**
   - High-level workflow management
   - Decides: upload, archive, validate, human_review, continue, complete
   - Returns: Next step + reasoning

**Prompt Engineering:**
- Uses structured prompts with clear instructions
- Requests JSON-formatted responses
- Includes context (HTML, previous actions, errors)
- Temperature control for determinism (0.2-0.7)
- Top-K and Top-P sampling for quality

**Integration with Ollama:**
```python
async def _call_ollama(prompt, temperature):
    async with httpx.AsyncClient(timeout=INFERENCE_TIMEOUT) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": "fara-7b",
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "top_p": FARA_TOP_P,
                "top_k": FARA_TOP_K,
                "repeat_penalty": FARA_REPEAT_PENALTY
            }
        )
```

---

### 3. BrowserController

**File:** `src/browser/controller.py`

**Purpose:** Manages all browser automation using Playwright.

**Key Responsibilities:**
- Browser lifecycle management
- Page navigation and interaction
- Element selection and manipulation
- File downloads
- Screenshot capture
- State extraction

**Main Methods:**

1. **`initialize()`**
   - Launches Chromium browser
   - Creates browser context
   - Sets viewport dimensions
   - Configures timeouts

2. **`goto(url)`**
   - Navigates to URL
   - Waits for network idle
   - Returns success/error status

3. **`click(selector)`**
   - Clicks element by CSS/XPath selector
   - Handles timeouts
   - Returns action result

4. **`fill(selector, value)`**
   - Fills input field
   - Clears existing content
   - Returns action result

5. **`download_file(trigger_selector)`**
   - Triggers download by clicking element
   - Waits for download completion
   - Saves file to downloads directory
   - Returns filename + filepath

6. **`get_page_state()`**
   - Extracts current page information
   - Returns: title, URL, HTML content, timestamp

7. **`screenshot(name)`**
   - Captures screenshot
   - Saves to downloads directory
   - Returns base64-encoded image data

8. **`execute_action(action_spec)`**
   - Unified action executor
   - Dispatches to appropriate method based on action type
   - Supported actions: click, fill, goto, wait, download, scroll, key, screenshot

**Action Specification Format:**
```json
{
  "action": "click|fill|goto|wait|download|scroll|key|screenshot",
  "selector": "CSS or XPath selector",
  "value": "value for fill/goto/key actions",
  "reason": "Human-readable explanation"
}
```

**Error Handling:**
- Timeouts configurable per action
- Detailed error messages
- Automatic retry logic (in Orchestrator)
- Screenshots on failure (optional)

---

### 4. OCRProcessor

**File:** `src/ocr/processor.py`

**Purpose:** Extracts text from images and documents using Tesseract OCR.

**Key Responsibilities:**
- Image-to-text conversion
- PDF-to-text extraction
- OCR result caching
- Text quality estimation
- OCR error correction

**Main Methods:**

1. **`extract_text_from_image(image_path, use_cache)`**
   - Loads image file (JPG, PNG, TIFF)
   - Runs Tesseract OCR
   - Estimates confidence
   - Caches result
   - Returns: raw text + confidence score

2. **`extract_text_from_pdf(pdf_path, use_cache)`**
   - Converts PDF pages to images
   - Runs OCR on each page
   - Combines all pages
   - Returns: combined text + per-page text + page count

3. **`clean_ocr_text(raw_text)`**
   - Removes extra whitespace
   - Fixes common OCR errors (0↔O, l↔1, rn↔m)
   - Normalizes punctuation spacing
   - Returns: cleaned text

4. **`_estimate_confidence(text)`**
   - Heuristic-based confidence scoring
   - Checks for suspicious patterns (repeated characters, unusual sequences)
   - Returns: confidence score (0.0-1.0)

**Caching Strategy:**
- MD5 hash of filepath as cache key
- JSON files stored in cache directory
- Cache includes: raw text, confidence, timestamp
- Speeds up repeated processing

**Common OCR Error Patterns:**
```python
replacements = {
    r'\b0(?=[A-Z])\b': 'O',          # 0 → O before capital letter
    r'(?<=[a-z])l(?=[a-z]{2,})': 'i', # l → i in middle of word
    r'rn\b': 'm'                      # rn → m at word end
}
```

---

### 5. DocumentPipeline

**File:** `src/ocr/pipeline.py`

**Purpose:** End-to-end document processing workflow.

**Key Responsibilities:**
- File type detection
- OCR orchestration
- Text cleaning
- Result packaging

**Main Methods:**

1. **`process_document(filepath)`**
   - Detects file type (PDF, image)
   - Routes to appropriate OCR processor
   - Cleans extracted text
   - Returns: structured result

**Processing Flow:**
```
Input File
    ↓
File Type Detection (.pdf, .jpg, .png, etc.)
    ↓
OCR Processing (Tesseract)
    ↓
Text Cleaning (regex + heuristics)
    ↓
Result Packaging
    ↓
{
  "status": "success",
  "source_file": "...",
  "raw_ocr_text": "...",
  "cleaned_text": "...",
  "confidence": 0.95
}
```

---

### 6. FastAPI Server

**File:** `src/api/server.py`

**Purpose:** REST API for external interactions and web dashboard.

**Endpoints:**

**Task Management:**
- `POST /tasks` - Create new task
- `GET /tasks` - List all tasks
- `GET /tasks/{task_id}` - Get task status
- `GET /tasks/{task_id}/result` - Get task result
- `GET /tasks/{task_id}/audit` - Get audit log

**File Management:**
- `GET /downloads` - List downloaded files
- `GET /downloads/{filename}` - Download specific file

**System:**
- `GET /health` - Health check
- `GET /system/config` - System configuration
- `GET /system/logs` - Recent logs

**Background Task Execution:**
```python
@app.post("/tasks")
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
    task_id = orchestrator.create_task(request.objective, request.params)
    background_tasks.add_task(orchestrator.execute_task, task_id)
    return {"task_id": task_id, "status": "queued"}
```

**Static File Serving:**
- Serves web dashboard from `/frontend/` directory
- index.html provides UI for monitoring and control

---

## Data Flow & Processing

### 1. Task Execution Flow

```
User Request (Web UI or API)
    ↓
Create Task (AutomationOrchestrator)
    ↓
Initialize Audit Logger
    ↓
[AGENTIC LOOP START]
    ↓
┌───────────────────────────────────────────┐
│ 1. OBSERVE                                │
│    - Get current page HTML, title, URL   │
│    - Extract visible elements             │
└────────────────┬──────────────────────────┘
                 ↓
┌───────────────────────────────────────────┐
│ 2. REASON (Fara-7B)                       │
│    - Analyze page state                   │
│    - Consider objective                   │
│    - Review previous actions              │
│    - Generate action sequence             │
└────────────────┬──────────────────────────┘
                 ↓
┌───────────────────────────────────────────┐
│ 3. ACT (Browser Controller)               │
│    - Execute each action                  │
│    - Handle failures with retries         │
│    - Request self-correction if needed    │
│    - Log all actions to audit trail       │
└────────────────┬──────────────────────────┘
                 ↓
┌───────────────────────────────────────────┐
│ 4. UPDATE                                 │
│    - Check for new downloads              │
│    - Process documents if found           │
│    - Extract structured data              │
│    - Update task state                    │
└────────────────┬──────────────────────────┘
                 ↓
    Iteration complete?
         ↙     ↘
       NO      YES
        ↓       ↓
    [LOOP]  Complete Task
              ↓
       Return Result
```

### 2. Document Processing Flow

```
File Downloaded
    ↓
Detect File Type
    ├─ PDF → Convert to images → OCR each page
    ├─ Image → Direct OCR
    └─ Other → Error
    ↓
Raw OCR Text
    ↓
Text Cleaning
    - Remove extra whitespace
    - Fix common OCR errors
    - Normalize punctuation
    ↓
Cleaned Text
    ↓
Document Classification (Fara-7B)
    - Identify document type
    - Calculate confidence
    ↓
Structured Extraction (Fara-7B)
    - Apply extraction schema
    - Extract specific fields
    - Validate data
    ↓
Store Extracted Data
    - Add to task.extracted_data
    - Log to audit trail
    ↓
Return Success
```

### 3. Self-Correction Flow

```
Action Fails (e.g., click on invalid selector)
    ↓
Log Failure
    ↓
Retry Count < MAX_RETRIES?
    ↙        ↘
  NO         YES
   ↓          ↓
Skip       Request Self-Correction (Fara-7B)
Action          ↓
            Analyze HTML
                ↓
            Generate Alternative Selectors
                ↓
            Update Action with New Selector
                ↓
            Retry Action
                ↓
            Success?
              ↙    ↘
            YES    NO
             ↓      ↓
          Continue  Retry with next selector
                    or skip if exhausted
```

---

## API Specification

### Authentication
Currently no authentication (localhost only). For production, implement:
- API keys
- OAuth 2.0
- JWT tokens

### Request/Response Format
- **Content-Type:** `application/json`
- **Response Format:** JSON
- **Error Format:** Standard HTTP status codes + error details

### Endpoints Detail

#### POST /tasks
**Create and execute automation task**

**Request Body:**
```json
{
  "objective": "Login to website and download documents",
  "params": {
    "wait_for_download": true,
    "headless": true,
    "extraction_schema": {
      "field1": "description",
      "field2": "description"
    }
  }
}
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": null
}
```

**Status Codes:**
- 200: Task created successfully
- 500: Server error

#### GET /tasks/{task_id}
**Get task status**

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "started_at": "2025-12-06T10:30:00Z",
  "completed_at": "2025-12-06T10:35:00Z",
  "error": null,
  "num_actions": 15
}
```

**Status Values:**
- `pending` - Created but not started
- `running` - Currently executing
- `completed` - Successfully finished
- `failed` - Error occurred

#### GET /tasks/{task_id}/result
**Get task execution result and extracted data**

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "status": "success",
    "iterations": 12,
    "extracted_data": {}
  },
  "error": null,
  "extracted_data": {
    "invoice_123.pdf": {
      "vendor_name": "Acme Corp",
      "invoice_number": "INV-2025-001",
      "amount": "1500.00",
      "date": "2025-12-06"
    }
  }
}
```

#### GET /tasks/{task_id}/audit
**Get detailed audit log**

**Response:**
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
    "input_context": "Login form detected",
    "fara_decision": [],
    "confidence": 0.92
  }
]
```

---

## Configuration Management

### Environment Variables (.env)

**Ollama Configuration:**
```bash
OLLAMA_BASE_URL=http://localhost:11434  # Ollama API endpoint
OLLAMA_MODEL=fara-7b                     # Model name
```

**Website Credentials:**
```bash
TARGET_WEBSITE_URL=https://example.com   # Target website
TARGET_USERNAME=your_username            # Login username
TARGET_PASSWORD=your_password            # Login password
```

**Browser Settings:**
```bash
BROWSER_HEADLESS=True                    # Run without GUI
BROWSER_TIMEOUT=30000                    # Timeout in milliseconds
BROWSER_VIEWPORT_WIDTH=1280              # Browser width
BROWSER_VIEWPORT_HEIGHT=720              # Browser height
```

**System Settings:**
```bash
DOWNLOAD_DIR=./downloads                 # Download location
CACHE_DIR=./cache                        # Cache location
LOG_DIR=./logs                           # Log location
MAX_RETRIES=3                           # Action retry count
INFERENCE_TIMEOUT=120                    # LLM timeout (seconds)
```

**Tesseract Configuration:**
```bash
TESSERACT_PATH=/usr/local/bin/tesseract  # Tesseract binary path
```

**API Settings:**
```bash
API_HOST=0.0.0.0                        # API bind address
API_PORT=8000                           # API port
API_DEBUG=False                         # Debug mode
```

### Configuration File (src/config.py)

**Additional Parameters:**
```python
# Fara-7B Inference Parameters
FARA_CONTEXT_WINDOW = 4096           # Maximum context tokens
FARA_TEMPERATURE = 0.7               # Sampling temperature (0.0-1.0)
FARA_TOP_P = 0.9                     # Nucleus sampling
FARA_TOP_K = 40                      # Top-K sampling
FARA_REPEAT_PENALTY = 1.1            # Repetition penalty
```

**Usage in Code:**
```python
from src.config import (
    OLLAMA_BASE_URL,
    BROWSER_HEADLESS,
    MAX_RETRIES
)
```

---

## Security Architecture

### Threat Model

**Assets to Protect:**
- User credentials
- Downloaded documents
- System logs (may contain sensitive data)
- API endpoints

**Threats:**
- Credential exposure
- Unauthorized API access
- Data exfiltration
- Log tampering
- Injection attacks

### Security Measures

#### 1. **Credential Management**
```python
# ✅ GOOD: Environment variables
TARGET_PASSWORD = os.getenv("TARGET_PASSWORD")

# ❌ BAD: Hardcoded
TARGET_PASSWORD = "my_password"  # Never do this
```

**Best Practices:**
- Use environment variables
- Never commit `.env` to version control
- Use secrets management (Vault, AWS Secrets Manager)
- Rotate credentials regularly
- Use least-privilege principles

#### 2. **Local-Only Execution**
- No cloud API calls (privacy-preserving)
- All processing on local machine
- No data leaves your environment
- Full control over data

#### 3. **Audit Logging**
- Every action logged with timestamp
- JSON format for easy parsing
- Immutable log files (append-only)
- Includes: actions, decisions, errors, extracted data

#### 4. **Input Validation**
```python
# Pydantic models validate all API inputs
class TaskRequest(BaseModel):
    objective: str
    params: Optional[Dict[str, Any]] = None
```

#### 5. **Browser Isolation**
- Each task uses separate browser context
- Cookies and cache isolated
- No persistence between tasks
- Clean state for each execution

### Production Security Checklist

- [ ] Use HTTPS for API (reverse proxy with SSL)
- [ ] Implement authentication (API keys, OAuth)
- [ ] Rate limiting on API endpoints
- [ ] Input sanitization for all user inputs
- [ ] Secrets management (not .env files)
- [ ] Network isolation (firewall rules)
- [ ] Log encryption at rest
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning
- [ ] Principle of least privilege (file permissions)

---

## Development Guide

### Setting Up Development Environment

1. **Clone Repository:**
```bash
git clone https://github.com/theanuragg/intelliquest.git
cd intelliquest
```

2. **Create Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

4. **Configure Environment:**
```bash
cp .env.example .env
nano .env  # Edit with your settings
```

5. **Install Ollama and Fara-7B:**
```bash
# Install from https://ollama.ai
ollama pull fara-7b
ollama serve
```

### Project Structure

```
intelliquest/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   └── orchestrator.py        # Main orchestrator
│   ├── reasoning/
│   │   ├── __init__.py
│   │   └── engine.py              # Fara-7B reasoning
│   ├── browser/
│   │   ├── __init__.py
│   │   └── controller.py          # Playwright automation
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── processor.py           # OCR processing
│   │   └── pipeline.py            # Document pipeline
│   ├── api/
│   │   ├── __init__.py
│   │   └── server.py              # FastAPI server
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py              # Logging utilities
│   ├── config.py                  # Configuration
│   └── __init__.py
├── frontend/
│   └── index.html                 # Web dashboard
├── examples/
│   ├── example_basic.py           # Basic example
│   ├── example_invoice.py         # Invoice processing
│   └── api_client.py              # API client example
├── logs/                          # Generated logs
├── downloads/                     # Downloaded files
├── cache/                         # OCR cache
├── docs/                          # Documentation
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore
├── README.md                      # User documentation
├── TECHNICAL_README.md            # This file
├── START_HERE.md                  # Quick start guide
├── QUICK_START.md                 # Command reference
└── INSTALLATION.md                # Installation guide
```

---

## Deployment Strategies

(Content continues with deployment instructions, performance optimization, testing, troubleshooting, etc.)

### Production Deployment Considerations

- Use reverse proxy (Nginx/Apache) for HTTPS
- Implement proper authentication and authorization
- Set up log rotation and monitoring
- Configure automatic backups
- Use process managers (systemd, supervisor)
- Container orchestration (Docker, Kubernetes)
- Load balancing for high availability
- Database for persistent storage (optional)

---

## Conclusion

IntelliQuest is a powerful, flexible, and extensible AI automation platform. This technical documentation provides the foundation for understanding, developing, and deploying the system in various environments.

### Key Takeaways

1. **Architecture:** Layered, async, agentic design for autonomous operation
2. **Components:** Modular design with clear separation of concerns
3. **Extensibility:** Multiple extension points for customization
4. **Security:** Local-first, privacy-preserving approach
5. **Performance:** Optimizable at multiple levels
6. **Production-Ready:** Docker, Kubernetes, systemd deployment options

### Next Steps

- **For Users:** See [README.md](README.md) and [QUICK_START.md](QUICK_START.md)
- **For Developers:** Review [examples/](examples/) and extend core components
- **For DevOps:** See Deployment Strategies section
- **For Security:** Review Security Architecture section

### Contributing

Contributions welcome! Focus areas:
- Additional document types and extractors
- Performance optimizations
- Security enhancements
- Test coverage
- Documentation improvements

---

**Maintained by:** IntelliQuest Team  
**License:** MIT  
**Repository:** [github.com/theanuragg/intelliquest](https://github.com/theanuragg/intelliquest)
