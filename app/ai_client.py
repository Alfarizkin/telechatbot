import httpx
from .config import GROQ_API_KEY

HF_URL = "https://api.groq.com/openai/v1/chat/completions"

async def ask_ai(messages: list[dict]) -> str:
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 1024
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_URL, json=payload, headers=headers)
        headers_info = response.headers
        
        retry = headers_info.get("retry-after")
        rpd_remaining = headers_info.get("x-ratelimit-remaining-requests")
        tpm_remaining = headers_info.get("x-ratelimit-remaining-tokens")
        rpd_reset = headers_info.get("x-ratelimit-reset-requests")
        tpm_reset = headers_info.get("x-ratelimit-reset-tokens")

        # Cetak Monitoring ke Terminal
        print("-" * 30)
        print(f"--- MONITORING LIMIT GROQ ---")
        print(f"Coba lagi setelah {retry}")
        print(f"Sisa Chat (Hari Ini)  : {rpd_remaining} (Reset dalam: {rpd_reset})")
        print(f"Sisa Token (Menit Ini): {tpm_remaining} (Reset dalam: {tpm_reset})")
        print("-" * 30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
