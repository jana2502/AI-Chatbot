from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    message_id: int

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: Optional[str] = "New Conversation"

class ConversationCreate(ConversationBase):
    user_id: int

# Basic conversation without messages (to avoid circular dependency)
class Conversation(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversation with messages (use this when you specifically need messages)
class ConversationWithMessages(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

# Basic user without conversations (this fixes your issue)
class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# User with conversations (use this when you specifically need conversations)
class UserWithConversations(UserBase):
    id: int
    created_at: datetime
    conversations: List[Conversation] = []
    
    class Config:
        from_attributes = True

# User with full conversation details (use sparingly)
class UserWithFullConversations(UserBase):
    id: int
    created_at: datetime
    conversations: List[ConversationWithMessages] = []
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    user_id: int

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    message_id: int