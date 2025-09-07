# FastAPI Gemini API

🚀 API FastAPI + Google Gemini

Este projeto implementa uma API com FastAPI integrada ao Google Gemini via google-generativeai.
O sistema expõe endpoints REST e um frontend simples em HTML para interação direta com o modelo de IA.

📌 Tecnologias utilizadas

FastAPI
 → Framework web moderno e rápido para Python.

Poetry
 → Gerenciador de dependências e ambiente virtual.

Uvicorn
 → Servidor ASGI para rodar a aplicação.

Google AI SDK
 → SDK oficial para integração com o modelo Gemini.

Python-dotenv
 → Carregamento de variáveis de ambiente (.env).

Froent-end com HTML e javascript básico:
Javascript utilizado pra fazer animação no box quando a IA está respondendo fica amarelo e quando dá a resposta fica verde.

Para rodar o codigo: 
poetry run uvicorn main:app --reload
