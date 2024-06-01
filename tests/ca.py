from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json
import yaml

load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("CA_KEY")
#     base_url="https://api.chatanywhere.tech/v1"
# )

url = "https://api.chatanywhere.tech/v1/chat/completions"

with open('content.yaml', 'r', encoding='utf-8') as f:
    content = yaml.safe_load(f)

payload = json.dumps({
    "model": "gpt-3.5-turbo-0125",
    "messages": [
        {
            "role": "system",
            "content": content['system']},
        {
            "role": "user",
            "content": content['user']},
        {
            "role": "assistant",
            "content": content['assistant']
        },
        {
            "role": "user",
            "content": content['input']
        }
    ]
})

headers = {
    'Authorization': f"Bearer {os.getenv('CA_KEY')}",
    'Content-Type': 'application/json'
    }

resp = requests.post(url, headers=headers, data=payload)

for item in resp.json()['choices']:
    print(item['message']['content'])

