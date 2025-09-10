import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY não encontrado no .env")

# Configura o SDK
genai.configure(api_key=API_KEY)

class GeminiService:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self._model = genai.GenerativeModel(model_name)

    def _call_model_blocking(self, prompt: str) -> str:
        response = self._model.generate_content(prompt)
        return getattr(response, "text", str(response))

    async def generate_gemini_response(self, prompt: str) -> str:
        return await asyncio.to_thread(self._call_model_blocking, prompt)
