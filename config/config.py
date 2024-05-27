import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
    CHAT_IDS = {
        "闲聊区@编程小白社": os.getenv("闲聊区@编程小白社"),
        "测试专用": os.getenv("测试专用"),
        "天明": os.getenv("天明"),
        "kevin-bot": os.getenv("kevin-bot"),
    }
    SCHEDULE_TIME = ["04:20", "05:00", "08:45", "08:50", "22:45"]