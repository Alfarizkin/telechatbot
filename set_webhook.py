import requests

BOT_TOKEN = "8089959411:AAESlQMiD5WftOMN1PgPaEb_hqMJeUXr3OE"
NGROK_URL = "https://suppletive-damion-dissociative.ngrok-free.dev"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": f"{NGROK_URL}/webhook"}

res = requests.post(url, data=payload)
print(res.json())
# https://e7cf0a9d4307.ngrok-free.app/chat/
# curl -X POST https://e7cf0a9d4307.ngrok-free.app/chat/ -H "Content-Type: application/json" -d "{\"user_character\":\"a\", \"ai_character\":\"b\", \"user_prompt\":\"halo\"}"