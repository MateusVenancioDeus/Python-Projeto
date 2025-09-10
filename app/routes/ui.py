from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home():
    project_root = Path(__file__).resolve().parent.parent.parent
    html_path = project_root / "frontend" / "index.html"

    if not html_path.exists():
        return HTMLResponse("<h1>Arquivo index.html não encontrado.</h1>", status_code=404)

    return FileResponse(str(html_path), media_type="text/html")
