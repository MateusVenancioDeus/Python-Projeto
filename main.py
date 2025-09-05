import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter chave da API do ambiente
api_key: str | None = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Chave da API não encontrada. Configure no arquivo .env")

# Configurar Google Gemini
genai.configure(api_key=api_key)

# Inicializar FastAPI
app = FastAPI(
    title="API FastAPI + Google Gemini",
    description="Camada intermediária para interação com o modelo Gemini via Google AI SDK",
    version="1.0.0"
)


# Modelos de dados para request e response
class PromptRequest(BaseModel):
    """Modelo de entrada do usuário para o prompt enviado ao Gemini."""
    prompt: str = Field(..., example="Explique o que é FastAPI em uma frase.")


class GeminiResponse(BaseModel):
    """Modelo de resposta retornado pela API Gemini."""
    input: str
    output: str
    model: str


# Frontend simples
@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    """
    Rota inicial que retorna a interface HTML simples de chat com Gemini.
    """
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <h1>Bem vindo ao Seu chat gratuito!<h1>
        <title>Chat com IA do google</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0D0D0D;
                margin: 0; padding: 0;
                display: flex; flex-direction: column; align-items: center;
                height: 100vh;
                justify-content: center;
            }
            h1 {
                color: #FFFFFF;
            }
            #chatbox {
                width: 90%;
                max-width: 600px;
                background: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }
            textarea {
                width: 100%;
                height: 100px;
                border-radius: 4px;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
                resize: vertical;
            }
            button {
                margin-top: 10px;
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007bff;
                border: none;
                color: white;
                border-radius: 4px;
                cursor: pointer;
            }
            button:disabled {
                background-color: #9e9e9e;
                cursor: not-allowed;
            }
            #response {
                margin-top: 20px;
                white-space: pre-wrap;
                background: #e9ecef;
                padding: 15px;
                border-radius: 4px;
                min-height: 80px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <h1>Chat com Google Gemini</h1>
        <div id="chatbox">
            <textarea id="prompt" placeholder="Digite sua pergunta aqui..."></textarea>
            <button id="sendBtn">Enviar</button>
            <div id="response"></div>
        </div>
        <script>
            const sendBtn = document.getElementById('sendBtn');
            const promptInput = document.getElementById('prompt');
            const responseDiv = document.getElementById('response');

            sendBtn.addEventListener('click', async () => {
                const promptText = promptInput.value.trim();
                if (!promptText) {
                    alert('Digite algo no prompt!');
                    return;
                }
                sendBtn.disabled = true;
                responseDiv.textContent = 'Carregando...';

                try {
                    const res = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ prompt: promptText })
                    });
                    if (!res.ok) {
                        const err = await res.json();
                        throw new Error(err.detail || 'Erro na requisição: ' + res.status);
                    }
                    const data = await res.json();
                    responseDiv.textContent = data.output;
                } catch (error) {
                    responseDiv.textContent = 'Erro: ' + error.message;
                } finally {
                    sendBtn.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    """

# Endpoint POST /ask
@app.post("/ask", response_model=GeminiResponse)
async def ask_gemini(request: PromptRequest) -> GeminiResponse:
    """
    Endpoint que envia o prompt do usuário para o modelo Gemini e retorna a resposta.

    - **prompt**: texto enviado pelo usuário (entrada).
    - **response**: texto gerado pelo modelo Gemini (saída).
    """
    try:
        model_name: str = "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)

        response = model.generate_content(request.prompt)

        # Extrair texto da resposta
        output_text: str = response.text if response.text else "[Sem resposta do modelo]"

        return GeminiResponse(
            input=request.prompt,
            output=output_text,
            model=model_name
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao consultar Gemini: {str(e)}")
