import requests
import json

url = "http://127.0.0.1:3001/v1/chat/completions"
headers = {"Authorization": "Bearer freellmapi-fe49f0db8eb45a3f06651fecb591c22b6082c2c69191a22a"}
payload = {
    "model": "local-model",
    "messages": [{"role": "user", "content": "You are ted. Say something short and in-character."}]
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
