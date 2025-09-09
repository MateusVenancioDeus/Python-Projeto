import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega .env
load_dotenv()

# Recupera chave
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Variável GOOGLE_API_KEY não encontrada no ambiente")

# Configura Gemini
genai.configure(api_key=api_key)

def generate_gemini_response(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
