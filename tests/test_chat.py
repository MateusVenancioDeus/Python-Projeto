import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


@pytest.mark.parametrize("prompt", [
    "Qual é a capital do Brasil?",
    "Explique o que é FastAPI em uma frase.",
    "Quem escreveu Dom Casmurro?",
    "Faça uma soma: 25 + 17"
])
def test_chat_real_flow(prompt):
    """
    Teste real (sem mock):
    1. Cliente envia requisição → endpoint FastAPI.
    2. API valida entrada (Pydantic).
    3. Serviço chama Google AI ADK de verdade.
    4. Resposta do Gemini é retornada em JSON.
    """

    # Cliente envia requisição
    response = client.post("/chat/ask", json={"prompt": prompt})

    # 2️⃣ API valida entrada
    assert response.status_code == 200

    # 4️⃣ Resposta real do Gemini
    data = response.json()
    print("\n🔹 Prompt:", prompt)
    print("🔹 Resposta do Gemini:", data["output"])

    # Verifica que há resposta
    assert "output" in data
    assert isinstance(data["output"], str)
    assert len(data["output"]) > 0
