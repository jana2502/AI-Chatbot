from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..ai_services import generate_ai_response  # Now uses Ollama

router = APIRouter(prefix="/chat", tags=["chat"])

def clean_ai_response(response: str) -> str:
    """Clean unwanted characters from AI response"""
    cleaned = response.replace('\\n', ' ')
    cleaned = ' '.join(cleaned.split())
    cleaned = cleaned.replace('\\t', ' ').replace('\\r', '')
    return cleaned.strip()

@router.post("/send", response_model=schemas.ChatResponse)
async def send_message(chat_request: schemas.ChatRequest, db: Session = Depends(get_db)):
    if chat_request.conversation_id:
        conversation = crud.get_conversation(db, chat_request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation_data = schemas.ConversationCreate(
            user_id=chat_request.user_id,
            title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
        )
        conversation = crud.create_conversation(db, conversation_data)
    
    user_message_data = {
        "conversation_id": conversation.id,
        "role": "user",
        "content": chat_request.message
    }
    user_message = crud.create_message(db, user_message_data)
    
    messages_history = crud.get_conversation_messages(db, conversation.id)
    ai_response = generate_ai_response(messages_history, chat_request.message)
    
    # Clean the AI response to remove unwanted \n characters
    cleaned_ai_response = clean_ai_response(ai_response)
    
    ai_message_data = {
        "conversation_id": conversation.id,
        "role": "assistant",
        "content": cleaned_ai_response
    }
    ai_message = crud.create_message(db, ai_message_data)
    
    return schemas.ChatResponse(
        response=cleaned_ai_response,
        conversation_id=conversation.id,
        message_id=ai_message.id
    )