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
    Html basico que retorna com o gemini ia.
    """
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Chat IA</title>
    <style>
    body {
      font-family: Arial, sans-serif;
      background: #121212;
      margin: 0; 
      padding: 0;
      display: flex; 
      flex-direction: column; 
      align-items: center;
      height: 100vh;
      justify-content: center;
    }

    h1 {
      color: #FFFFFF;
      text-align: center;
    }

    #chatbox {
      width: 90%;
      max-width: 600px;
      background: #121212;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }

    textarea, #response {
      width: 100%;
      height: 150px;   /* altura fixa */
      border-radius: 6px;
      border: 3px solid #ccc; /* borda mais grossa */
      padding: 10px;
      font-size: 16px;
      resize: none;    
      box-sizing: border-box;
    }

    textarea {
      background: #fff;
      color: #000;
    }

    #response {
      background: #e9ecef;
      color: #000;
      overflow-y: auto;
      margin-top: 20px; /* deixa mais afastado do botão */
      border: 3px solid transparent; /* borda invisível por padrão */
      transition: border 0.3s ease-in-out;
    }

    /* amarelo enquanto responde */
    #response.responding {
      border: 3px solid yellow;
    }

    /* verde quando terminou */
    #response.completed {
      border: 3px solid limegreen;
    }

    button {
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

      // reset ciclo
      responseDiv.classList.remove('completed');
      responseDiv.textContent = 'IA respondendo...';
      responseDiv.classList.add('responding');

      sendBtn.disabled = true;

      try {
        const res = await fetch('/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: promptText })
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Erro na requisição: ' + res.status);
        }

        const data = await res.json();
        responseDiv.textContent = data.output;

        // aplica borda verde permanente
        responseDiv.classList.remove('responding');
        responseDiv.classList.add('completed');

      } catch (error) {
        responseDiv.textContent = 'Erro: ' + error.message;
        responseDiv.classList.remove('responding');
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
