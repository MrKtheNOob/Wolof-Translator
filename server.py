from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from translator import FrenchWolofTranslator
from config import ModelConfig
from env_config import EnvConfig

app = FastAPI(title="Wolof-NMT API")

# Global translator variable
translator = None

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "fr"  # "fr" for French to Wolof, "wo" for Wolof to French

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str

@app.lifespan("startup")
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

if __name__ == "__main__":
    # Note: On a t3.medium (4GB RAM), we must use only 1 worker
    uvicorn.run(app, host="0.0.0.0", port=8000)
