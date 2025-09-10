from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path

# importa as rotas
from app.routes.chat import router as chat_router
from app.routes.ui import router as ui_router

# carrega variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="API FastAPI + Google Gemini",
    description="Chat com Google Gemini (SDK) usando frontend estilizado",
    version="1.0.0"
)

# inclui as rotas
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(ui_router, prefix="/ui", tags=["ui"])

# frontend
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_PATH = FRONTEND_DIR / "index.html"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    if INDEX_PATH.exists():
        return FileResponse(str(INDEX_PATH), media_type="text/html")
    return HTMLResponse("<h1>index.html não encontrado.</h1>", status_code=404)
