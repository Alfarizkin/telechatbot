import httpx
from .config import OPENROUTER_API_KEY

async def ask_ai(message: str) -> str:
    payload= {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": message}]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        result = response.json()
        return result["choices"][0]["message"]["content"]