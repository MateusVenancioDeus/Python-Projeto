from fastapi import APIRouter
import google.generativeai as genai

router = APIRouter()
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

@router.post("/chat")
async def chat_with_gemini(prompt: str):
    response = chat.send_message(prompt)
    return {"prompt": prompt, "response": response.text}
