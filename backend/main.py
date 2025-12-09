from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# Import our services
from paddleocr_service import manga_ocr
from ernie_service import get_ernie_translator

app = FastAPI(title="Translator Gator API")

# CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    image_url: str
    mode: str = "natural"

class Bubble(BaseModel):
    x: int
    y: int
    width: int
    height: int
    original_text: str
    translated_text: str

class TranslationResponse(BaseModel):
    bubbles: List[Bubble]
    success: bool

# Initialize ERNIE model on startup
ernie_translator = None

@app.on_event("startup")
async def startup_event():
    """Load ERNIE model on startup"""
    global ernie_translator
    model_name = os.getenv("ERNIE_MODEL", "baidu/ERNIE-4.5-8B-Instruct")
    print(f"Initializing ERNIE model: {model_name}")
    ernie_translator = get_ernie_translator(model_name)
    print("ERNIE model ready!")

@app.get("/")
def root():
    return {
        "message": "Translator Gator API is running! 🐊",
        "model": "ERNIE 4.5 from Hugging Face",
        "ocr": "PaddleOCR-VL"
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate_manga(request: TranslationRequest):
    """
    Main translation endpoint
    1. Extract text with PaddleOCR-VL
    2. Translate with ERNIE from Hugging Face
    3. Return bubble coordinates + translations
    """
    try:
        # Step 1: OCR with PaddleOCR
        ocr_results = manga_ocr.extract_from_url(request.image_url)
        
        # Step 2: Translate with ERNIE
        bubbles = []
        for result in ocr_results:
            translated = ernie_translator.translate(
                result['text'],
                request.mode
            )
            
            bubble = Bubble(
                x=result['x'],
                y=result['y'],
                width=result['width'],
                height=result['height'],
                original_text=result['text'],
                translated_text=translated
            )
            bubbles.append(bubble)
        
        return TranslationResponse(bubbles=bubbles, success=True)
    
    except Exception as e:
        print(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Check if models are loaded"""
    return {
        "status": "healthy",
        "ernie_loaded": ernie_translator is not None,
        "ocr_loaded": manga_ocr is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
