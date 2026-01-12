import httpx
from .config import HF_API_TOKEN

HF_URL = "https://router.huggingface.co/v1/chat/completions"

async def ask_ai(messages: list[dict]) -> str:
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
