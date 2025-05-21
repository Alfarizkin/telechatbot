import httpx
from .config import OPENROUTER_API_KEY

async def ask_ai(prompt: str) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    timeout = httpx.Timeout(30.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except httpx.ReadTimeout:
        return "Server terlalu lama merespons. Silakan coba lagi nanti."
    except httpx.HTTPStatusError as e:
        return f"Gagal dari server: {e.response.status_code}"
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"