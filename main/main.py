from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel
from services.gemini_client import generate_gemini_response
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = FastAPI(
    title="API FastAPI + Google Gemini",
    description="Chat com Google Gemini (ADK) usando frontend estilizado",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def home():
    project_root = Path(__file__).resolve().parent.parent
    html_path = project_root / "frontend" / "index.html"
    if not html_path.exists():
        return HTMLResponse("<h1>Arquivo index.html não encontrado.</h1>", status_code=404)
    return html_path.read_text(encoding="utf-8")

class PromptInput(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(input: PromptInput):
    try:
        response = generate_gemini_response(input.prompt)
        return {"output": response}
    except Exception as e:
        return {"output": f"Erro ao gerar resposta: {str(e)}"}
