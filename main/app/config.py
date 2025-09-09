import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Chave da API não encontrada. Configure no arquivo .env")
