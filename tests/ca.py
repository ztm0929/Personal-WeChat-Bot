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

title_list = [
    "20、暑期实习 | 中国工商银行2024年星令营暑期实习正式启动！",
    "21、快报名！星巴克深圳校园门店招募日正式启动",
    "22、快到退休年龄，但养老保险没缴满15年，能一次性补齐吗？",
    "23、缺人！这些制造业企业急招500人",
    "24、5.30【深圳&全国】招聘实习大礼包",
    "25、科大讯飞24届春招正在进行中！",
    "26、国家城安院、深圳城安院岳清瑞院士团队 全球揽才招聘博士后正在进行中！",
    "27、现场报道||蚌埠市“2024年招才引智高校行”活动成功举办!",
    "28、河北金租2025届暑期实习生招聘正在进行中！",
    "29、广东省通信管理局局属单位2024年度公开招聘正在进行中！",
    "30、天健2024暑期实习培训生计划正在进行中！"
]

with open('tests/content.yaml', 'r', encoding='utf-8') as f:
    content = yaml.safe_load(f)

# 循环请求title_list中的每一个title

# 1. 请求聊天接口
# 2. 解析返回的数据
# 3. 打印assistant的回复

for title in title_list:
    payload = json.dumps({
        "model": "gpt-3.5-turbo-0125",
        "messages": [
            {
                "role": "system",
                "content": content['system']
            },
            {
                "role": "user",
                "content": content['user']
            },
            {
                "role": "assistant",
                "content": content['assistant']
            },
            {
                "role": "user",
                "content": title
            }
        ]
    })

    headers = {
        'Authorization': f"Bearer {os.getenv('CA_KEY')}",
        'Content-Type': 'application/json'
        }

    resp = requests.post(url, headers=headers, data=payload)
    assistant_reply = resp.json()['choices'][0]['message']['content']
    print(json.loads(assistant_reply)['is_recruit'])    
