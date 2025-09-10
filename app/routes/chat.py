from fastapi import APIRouter, HTTPException
from app.models.prompt_input import PromptInput
from app.services.gemini_client import GeminiService

router = APIRouter()

_gemini = GeminiService()

@router.post("/ask")
async def ask(input: PromptInput):
    try:
        response_text = await _gemini.generate_gemini_response(input.prompt)
        return {"output": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

