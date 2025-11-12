from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.firebase_service import FirebaseService
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/api/chat", tags=["chat"])

firebase_service = FirebaseService()
gemini_service = GeminiService()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    
    Accepts a user message and optional conversation history,
    returns an AI-generated response based on current gait data
    """
    try:
        # Fetch latest gait data
        gait_data = firebase_service.get_all_data()
        
        # Generate AI response
        response = gemini_service.generate_response(
            user_message=request.message,
            gait_data=gait_data,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            response=response,
            gait_data_summary=gait_data.get("current")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.get("/gait-data")
async def get_gait_data():
    """Endpoint to fetch current gait data"""
    try:
        data = firebase_service.get_all_data()
        if not data.get("current"):
            raise HTTPException(status_code=404, detail="No gait data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Gait Chatbot API is running"
    )