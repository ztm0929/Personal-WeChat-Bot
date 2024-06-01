from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("CA_KEY")
#     base_url="https://api.chatanywhere.tech/v1"
# )

url = "https://api.chatanywhere.tech/v1/chat/completions"

payload = json.dumps({
    "model": "gpt-4o-2024-05-13",
    "messages": [
        {
            "role": "system",
            "content": "用一致的风格拒绝别人，充满嘲讽和挖苦的语气~"
        },
        {
            "role": "user",
            "content": "今天天气怎么样?"
        },
        {
            "role": "assistant",
            "content": "我不知道任何信息，你自己查去！"
        },
        {
            "role": "user",
            "content": "2023年NBA总冠军是谁？"
        
        }
    ]
})

headers = {
    'Authorization': f"Bearer {os.getenv('CA_KEY')}",
    'Content-Type': 'application/json'
    }

resp = requests.post(url, headers=headers, data=payload)

print(resp.json())


