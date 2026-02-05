# PersonaGPT

A real-time AI chatbot built with **FastAPI** and **OpenAI's GPT-4o Mini** model. It features a clean, dark-themed chat interface served directly from the backend — no separate frontend framework needed.

## What It Does

- Accepts user messages through a chat UI and returns AI-generated responses using OpenAI's GPT-4o Mini model.
- Maintains conversation history per session so the AI remembers context within a chat.
- Provides a "New Chat" button to reset the conversation and start fresh.

## Tech Stack

- **Backend:** FastAPI + Uvicorn (ASGI)
- **AI Model:** OpenAI GPT-4o Mini
- **Frontend:** Single-page HTML/CSS/JS (served as a static file)
- **Validation:** Pydantic v2

## Project Structure

```
PersonaGPT/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── api/routes/chat.py     # Chat API endpoints
│   ├── core/config.py         # Environment config (API key, model)
│   ├── schemas/chat.py        # Request/Response Pydantic models
│   └── services/chatbot.py    # OpenAI integration logic
├── static/
│   └── index.html             # Chatbot UI
├── .env.example               # Environment variable template
├── requirements.txt           # Python dependencies
└── README.md
```

## API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| GET    | `/`               | Serves the chatbot UI              |
| POST   | `/api/chat/send`  | Send a message and get AI reply    |
| POST   | `/api/chat/reset` | Reset the conversation history     |
| GET    | `/health`         | Health check                       |

## Setup

### Step 1 — Clone and Create Virtual Environment

```bash
git clone https://github.com/Harshprajapat777/PersonaGPT.git
cd PersonaGPT
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Add Your OpenAI API Key

Copy the example env file and add your key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual key:

```
OPENAI_API_KEY=your-openai-api-key-here
```

You can get an API key from [platform.openai.com](https://platform.openai.com/api-keys).

### Step 4 — Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

### Step 5 — Open the Chat

Go to **http://localhost:8000** in your browser. Start chatting.

## Connectivity

The app needs two things to work:

1. **Internet connection** — Required for making API calls to OpenAI's servers. The backend sends your messages to OpenAI and streams back the response.
2. **Valid OpenAI API key** — You must have an active API key with available credits. If the key is missing or invalid, the chat will return a 500 error with details.

### How It Connects

```
Browser (localhost:8000)
    │
    │  POST /api/chat/send  { "message": "Hello" }
    ▼
FastAPI Server
    │
    │  OpenAI Python SDK → HTTPS request
    ▼
OpenAI API (api.openai.com)
    │
    │  GPT-4o Mini generates response
    ▼
FastAPI Server
    │
    │  { "reply": "Hi! How can I help?" }
    ▼
Browser (renders in chat UI)
```

### Troubleshooting

| Issue | Fix |
|---|---|
| `401 Unauthorized` | Your API key is invalid. Check `.env`. |
| `429 Rate Limit` | You've exceeded OpenAI rate limits. Wait or upgrade your plan. |
| `500 Internal Server Error` | Check the terminal for the full error traceback. |
| Chat UI doesn't load | Make sure the server is running on port 8000. |
| No response from AI | Check your internet connection and API key credits. |
