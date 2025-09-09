from pydantic import BaseModel, Field
class GeminiResponse(BaseModel):
    input_text: str = Field(..., examples=["Explique o que é FastAPI em uma frase."])
    output: str = Field(..., examples=["FastAPI é um framework web moderno e rápido para construir APIs com Python."])
    model: str = Field(..., examples=["gemini-1.5-flash"])
response = GeminiResponse(
    input_text="Explique o que é FastAPI em uma frase.",
    output="FastAPI é um framework web moderno e rápido para construir APIs com Python.",
    model="gemini-1"
)
print(response)