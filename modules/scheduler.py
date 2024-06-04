import schedule
import time
import logging
from threading import Thread
from .api.coin_rank import CoinRank
from .api.github_trending import GitHubTrending
from dotenv import load_dotenv
import os
from .rss import push_updates


load_dotenv()

def schedule_messages(send_text_func, send_rich_text_func):
    coin_rank = CoinRank(api_key=os.getenv("COINGECKO_API_KEY"))
    github_trending = GitHubTrending()

    """
    定时发送消息的函数
    """
    times = ["04:00", "06:26", "08:45", "12:15", "08:50", "22:45"]
    messages = [
        (coin_rank.get_coin_rank, "wxid_92woynyarvut21", ''),
        (github_trending.get_trending_repositories, "wxid_92woynyarvut21", ''),
        ("[Sun]GM", os.getenv("闲聊区@编程小白社"), ''),
        (github_trending.get_trending_repositories, os.getenv("闲聊区@编程小白社"), ''),
        (coin_rank.get_coin_rank, os.getenv("闲聊区@编程小白社"), ''),
        ("[Moon]GN", os.getenv("闲聊区@编程小白社"), '')
    ]
    
    def create_task(message_func, chat_id, additional):
        if callable(message_func):
            return lambda: send_text_func(message_func(), chat_id, additional)
        else:
            return lambda: send_text_func(message_func, chat_id, additional)

    for time_str, (message_func, chat_id, additional) in zip(times, messages):
        task = create_task(message_func, chat_id, additional)
        schedule.every().day.at(time_str).do(task)
    
    rss_times = ["12:10", "18:10", "22:10"]
    for time_str in rss_times:
        schedule.every().day.at(time_str).do(lambda: send_text_func(push_updates(), "50453454101@chatroom", '') )

    schedule.every(30).seconds.do(lambda: send_text_func("Hello, World!", "wxid_92woynyarvut21", ''))
    schedule.every(30).seconds.do(lambda: send_rich_text_func("Test", "", "Test", "Test", "https://www.google.com", "", os.getenv("测试专用")) )

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"程序运行时发生错误: {e}")
            logging.info("程序将在60秒后重试。")
            time.sleep(60)

def start_scheduler(send_text_func, send_rich_text_func):
    """
    启动定时任务调度器
    """
    Thread(target=schedule_messages, args=(send_text_func, send_rich_text_func), name="PeriodicMessageThread", daemon=True).start()
