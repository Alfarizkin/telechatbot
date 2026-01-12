import requests
import json

response = requests.get(
  url="https://openrouter.ai/api/v1/key",
  headers={
    "Authorization": "Bearer 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"
  }
)

print(json.dumps(response.json(), indent=2))
