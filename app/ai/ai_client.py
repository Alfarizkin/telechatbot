import httpx
from ..cores.config import GROQ_API_KEY

HF_URL = "https://api.groq.com/openai/v1/chat/completions"

async def ask_ai(messages: list[dict]) -> str:
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.85,
        "top_p": 0.9,
        "frequency_penalty": 0.3,
        "presence_penalty": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_URL, json=payload, headers=headers)

        headers_info = response.headers
        print("-" * 30)
        print(f"--- MONITORING LIMIT GROQ ---")
        print(f"Coba lagi setelah {headers_info.get("retry-after") or '-'}")
        print(f"Sisa Chat (Hari Ini)  : {headers_info.get("x-ratelimit-remaining-requests")} (Reset dalam: {headers_info.get("x-ratelimit-reset-requests")})")
        print(f"Sisa Token (Menit Ini): {headers_info.get("x-ratelimit-remaining-tokens")} (Reset dalam: {headers_info.get("x-ratelimit-reset-tokens")})")
        print("-" * 30)
        
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            print(response.text)
            raise
        return response.json()["choices"][0]["message"]["content"]
        
