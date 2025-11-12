from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat
from app.config.settings import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Gait Analysis Chatbot API",
    description="AI-powered chatbot for gait analysis using Gemini AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Gait Analysis Chatbot API",
        "docs": "/docs",
        "health": "/api/chat/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)