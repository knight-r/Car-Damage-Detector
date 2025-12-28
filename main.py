from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models.schemas import CarDamageResponse, ErrorResponse
from services.image_processor import ImageProcessor
from services.llm_service import llm_service
from config import config

# Validate configuration on startup
config.validate()

app = FastAPI(
    title="Car Damage Detection API",
    description="AI-powered car damage detection using OpenAI GPT-4 Vision",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Car Damage Detection API",
        "version": "1.0.0",
        "model": config.OPENAI_MODEL,
        "endpoints": {
            "analyze": "/analyze - POST - Analyze car damage from images",
            "health": "/health - GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": config.OPENAI_MODEL,
        "api_configured": bool(config.OPENAI_API_KEY)
    }

@app.post("/analyze", response_model=List[CarDamageResponse])
async def analyze_car_damage(
    files: List[UploadFile] = File(..., description="Car images to analyze"),
    custom_prompt: Optional[str] = Form(None, description="Additional analysis instructions")
):
    """
    Analyze car damage from uploaded images using OpenAI GPT-4 Vision.
    
    Returns structured JSON with damage details including:
    - Damage type
    - Bounding box coordinates
    - Severity rating (1-5)
    - Detailed description
    """
    try:
        # Validate at least one file
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Process images
        processed_images = await ImageProcessor.process_multiple_images(files)
        
        # Analyze with OpenAI
        results = await llm_service.analyze_car_damage(
            processed_images,
            custom_prompt=custom_prompt
        )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)