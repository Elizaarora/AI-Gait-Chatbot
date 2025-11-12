from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    """Single chat message"""
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    message: str
    conversation_history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    response: str
    gait_data_summary: Optional[dict] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str