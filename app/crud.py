from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_conversation(db: Session, conversation: schemas.ConversationCreate):
    db_conversation = models.Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()

def get_user_conversations(db: Session, user_id: int):
    return db.query(models.Conversation).filter(
        models.Conversation.user_id == user_id
    ).all()

def create_message(db: Session, message_data: dict):
    db_message = models.Message(**message_data)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_conversation_messages(db: Session, conversation_id: int):
    return db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.timestamp).all()