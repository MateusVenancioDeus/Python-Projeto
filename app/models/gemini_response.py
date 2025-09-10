from pydantic import BaseModel, Field

class GeminiResponse(BaseModel):
    input_text: str = Field(..., example="Explique o que é FastAPI em uma frase.")
    output: str = Field(..., example="FastAPI é um framework web moderno e rápido para construir APIs com Python.")
    model: str = Field(..., example="gemini-1.5-flash")