import schedule
import time
import logging
from threading import Thread
from .api.coin_rank import CoinRank
from dotenv import load_dotenv
import os


load_dotenv()

def schedule_messages(send_message_func):
    coin_rank = CoinRank(api_key=os.getenv("COINGECKO_API_KEY"))

    """
    定时发送消息的函数
    """
    times = ["04:00", "05:00", "08:45", "08:50", "22:45"]
    messages = [
        (coin_rank.get_coin_rank, "wxid_92woynyarvut21", ''),
        (coin_rank.get_coin_rank, "wxid_92woynyarvut21", ''),
        ("[Sun]GM", os.getenv("闲聊区@编程小白社"), ''),
        (coin_rank.get_coin_rank, os.getenv("闲聊区@编程小白社"), ''),
        ("[Moon]GN", os.getenv("闲聊区@编程小白社"), '')
    ]
    
    def create_task(message_func, chat_id, additional):
        if callable(message_func):
            return lambda: send_message_func(message_func(), chat_id, additional)
        else:
            return lambda: send_message_func(message_func, chat_id, additional)

    for time_str, (message_func, chat_id, additional) in zip(times, messages):
        task = create_task(message_func, chat_id, additional)
        schedule.every().day.at(time_str).do(task)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"程序运行时发生错误: {e}")
            logging.info("程序将在60秒后重试。")
            time.sleep(60)

def start_scheduler(send_message_func):
    """
    启动定时任务调度器
    """
    Thread(target=schedule_messages, args=(send_message_func,), name="PeriodicMessageThread", daemon=True).start()