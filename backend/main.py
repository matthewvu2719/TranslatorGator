from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import asyncio

from paddleocr_service import manga_ocr
from ernie_service import get_ernie_translator, ERNIETranslator

app = FastAPI(title="Translator Gator API")

# CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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

# Initialize ERNIE singleton
ernie_translator: Optional[ERNIETranslator] = None

@app.on_event("startup")
async def startup_event():
    global ernie_translator
    model_name = os.getenv("ERNIE_MODEL", "baidu/ERNIE-4.5-0.3B-PT")
    print(f"[Startup] Loading ERNIE model: {model_name}")
    ernie_translator = get_ernie_translator(model_name)
    print("[Startup] ERNIE ready!")

@app.get("/")
def root():
    return {
        "message": "Translator Gator API running! 🐊",
        "model": "ERNIE 0.3B/3B",
        "ocr": "PaddleOCR-VL"
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate_manga(request: TranslationRequest):
    try:
        print(f"[API] Translating: {request.image_url[:80]}...")
        
        ocr_results = manga_ocr.extract_from_url(request.image_url)
        print(f"[API] OCR found {len(ocr_results)} text regions")
        
        if not ocr_results:
            return TranslationResponse(bubbles=[], success=True)

        async def translate_bubble(b):
            print(f"[API] Translating: {b['text'][:50]}...")
            translated = await asyncio.to_thread(ernie_translator.translate, b['text'], request.mode)
            print(f"[API] Result: {translated[:50]}...")
            return Bubble(
                x=b['x'], y=b['y'],
                width=b['width'], height=b['height'],
                original_text=b['text'], translated_text=translated
            )

        bubbles = await asyncio.gather(*[translate_bubble(b) for b in ocr_results])
        print(f"[API] Translation complete: {len(bubbles)} bubbles")
        return TranslationResponse(bubbles=list(bubbles), success=True)

    except Exception as e:
        import traceback
        print(f"[API] ERROR: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "ernie_loaded": ernie_translator is not None,
        "ocr_loaded": manga_ocr is not None
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global error handler for better debugging"""
    print(f"[ERROR] {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "success": False}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
