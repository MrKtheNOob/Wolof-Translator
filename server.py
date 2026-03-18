from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from translator import FrenchWolofTranslator
from config import ModelConfig
from env_config import EnvConfig

app = FastAPI(title="Wolof-NMT API")

# Ensure static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Global translator variable
translator = None

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "fr"  # "fr" for French to Wolof, "wo" for Wolof to French

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str

@app.on_event("startup")
async def load_model():
    """Load the model into memory on startup."""
    global translator
    model_checkpoint = EnvConfig.MODEL_CHECKPOINT()
    print(f"Loading model: {model_checkpoint} ...")
    try:
        translator = FrenchWolofTranslator(
            model_checkpoint=model_checkpoint,
            model_config=ModelConfig()
        )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "model": EnvConfig.MODEL_CHECKPOINT(),
        "ready": translator is not None
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    if translator is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    try:
        result = translator.translate(
            request.text, 
            source_lang=request.source_lang
        )
        return TranslationResponse(
            original_text=request.text,
            translated_text=result,
            source_lang=request.source_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount the static directory for other assets if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
