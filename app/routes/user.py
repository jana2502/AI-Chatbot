from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# Basic user info without conversations
@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get user with their conversations (separate endpoint)
@router.get("/{user_id}/with-conversations", response_model=schemas.UserWithConversations)
def get_user_with_conversations(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get user conversations separately (recommended approach)
@router.get("/{user_id}/conversations", response_model=list[schemas.Conversation])
def get_user_conversations(user_id: int, db: Session = Depends(get_db)):
    # First check if user exists
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Then get their conversations
    conversations = crud.get_user_conversations(db, user_id=user_id)
    return conversations