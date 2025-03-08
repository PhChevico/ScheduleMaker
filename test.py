import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
  },
  data=json.dumps({
    "model": "google/gemini-2.0-flash-thinking-exp:free", # Optional
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

print(response.text)