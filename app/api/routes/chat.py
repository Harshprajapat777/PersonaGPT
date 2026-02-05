from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot import get_chat_response

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory conversation history (per server session)
conversation_history: list[dict] = [
    {"role": "system", "content": "You are PersonaGPT, a helpful and friendly AI assistant."}
]


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    try:
        conversation_history.append({"role": "user", "content": request.message})
        reply = get_chat_response(conversation_history)
        conversation_history.append({"role": "assistant", "content": reply})
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_conversation():
    conversation_history.clear()
    conversation_history.append(
        {"role": "system", "content": "You are PersonaGPT, a helpful and friendly AI assistant."}
    )
    return {"message": "Conversation reset"}
