import requests

BOT_TOKEN = "8089959411:AAESlQMiD5WftOMN1PgPaEb_hqMJeUXr3OE"
NGROK_URL = "https://0d22-2001-448a-2070-2ee6-cda0-92a6-4a1-ac7e.ngrok-free.app"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
payload = {"url": f"{NGROK_URL}/webhook"}

res = requests.post(url, data=payload)
print(res.json())