from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from app.routes import user, chats

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Chatbot API",
    description="A FastAPI-based AI chatbot with PostgreSQL storage",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chats.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "AI Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}