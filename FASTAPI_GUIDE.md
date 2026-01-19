# FastAPI Architecture & Getting Started Guide

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework for building APIs. It's built on top of **Starlette** (for web parts) and **Pydantic** (for data validation).

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT REQUEST                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    UVICORN (ASGI Server)                │
│         (Handles async requests, runs the app)          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI APPLICATION                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │              MIDDLEWARE LAYER                    │    │
│  │    (CORS, Authentication, Logging, etc.)        │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │                   ROUTER                         │    │
│  │     (Routes requests to correct endpoints)       │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │              DEPENDENCY INJECTION                │    │
│  │    (Database sessions, Auth, Services, etc.)    │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │              PATH OPERATIONS                     │    │
│  │         (Your endpoint functions)                │    │
│  │    @app.get(), @app.post(), etc.                │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │           PYDANTIC MODELS (Schemas)             │    │
│  │    (Request/Response validation & serialization) │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   SERVICE LAYER                          │
│            (Business logic, AI/ML calls)                 │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                             │
│        (Database, External APIs, Cache, etc.)           │
└─────────────────────────────────────────────────────────┘
```

---

## Request-Response Flow

```
1. Client sends HTTP request
        ↓
2. UVICORN receives request (ASGI server)
        ↓
3. Middleware processes request (auth, CORS, logging)
        ↓
4. Router matches URL to endpoint function
        ↓
5. Dependencies are resolved (DB session, current user, etc.)
        ↓
6. Pydantic validates request body/params
        ↓
7. Endpoint function executes business logic
        ↓
8. Response is serialized via Pydantic
        ↓
9. Middleware processes response
        ↓
10. Client receives JSON response
```

---

## Project Folder Structure

```
PersonaGPT/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance & startup
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── chat.py      # Chat endpoints
│   │       └── health.py    # Health check endpoint
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings & environment variables
│   │   └── security.py      # Auth utilities (if needed)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py          # Database models (SQLAlchemy/etc)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py          # Pydantic models for request/response
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── chatbot.py       # Business logic (AI/LLM integration)
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py       # Utility functions
│
├── requirements.txt
├── .env                     # Environment variables
└── README.md
```

---

## Key Concepts

### 1. ASGI (Asynchronous Server Gateway Interface)
FastAPI uses ASGI instead of WSGI. This allows:
- **Async/await** support
- **WebSockets**
- **Background tasks**
- High concurrency with minimal resources

### 2. Dependency Injection
```python
# Dependencies are functions that provide resources
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Used in endpoints
@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### 3. Pydantic Schemas
```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
```

### 4. Routers (Modular Endpoints)
```python
# In api/routes/chat.py
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send")
async def send_message(request: ChatRequest):
    ...

# In main.py
from app.api.routes import chat
app.include_router(chat.router)
```

---

## How to Start

### Step 1: Install Dependencies
```bash
pip install fastapi uvicorn pydantic python-dotenv
```

### Step 2: Create Basic App (app/main.py)
```python
from fastapi import FastAPI

app = FastAPI(title="PersonaGPT", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to PersonaGPT"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Step 3: Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Access
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Linking Components Together

```
main.py
   │
   ├── includes routers from ──► api/routes/*.py
   │
   ├── loads config from ──────► core/config.py
   │
   └── registers middleware

routes/*.py
   │
   ├── uses schemas from ──────► schemas/*.py (validation)
   │
   ├── calls services from ────► services/*.py (business logic)
   │
   └── uses dependencies ──────► Depends(get_db), etc.

services/*.py
   │
   ├── uses models from ───────► models/*.py (database)
   │
   └── uses utils from ────────► utils/*.py (helpers)
```

---

## For Your Chatbot

Typical flow for a chat endpoint:

```
POST /chat/send
     │
     ▼
┌─────────────────┐
│ ChatRequest     │  ← Pydantic validates input
│ (schema)        │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ chat_router     │  ← Route handler receives request
│ (routes)        │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ ChatbotService  │  ← Business logic (call LLM, process)
│ (services)      │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ ChatResponse    │  ← Pydantic serializes output
│ (schema)        │
└─────────────────┘
     │
     ▼
JSON Response to Client
```

---

## Summary

| Layer | Purpose | Location |
|-------|---------|----------|
| **main.py** | App entry point, startup | `app/main.py` |
| **Routes** | HTTP endpoints | `app/api/routes/` |
| **Schemas** | Request/Response validation | `app/schemas/` |
| **Services** | Business logic | `app/services/` |
| **Models** | Database tables | `app/models/` |
| **Core** | Config, security | `app/core/` |
| **Utils** | Helper functions | `app/utils/` |

FastAPI follows a **layered architecture** pattern - keeping concerns separated makes code maintainable and testable.
