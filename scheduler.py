import schedule
import time
import logging
from threading import Thread
import requests

def get_bitcoin_price():
    url = (
        'https://api.coingecko.com/api/v3/simple/price'
        '?ids=bitcoin'
        '&vs_currencies=cny'
        '&include_last_updated_at=true'
        )

    res = requests.get(url)
    return res.text

def schedule_messages(send_message_func):
    """
    定时发送消息的函数
    """
    schedule.every().day.at("08:00").do(send_message_func, "这是定时发送的消息", "wxid_92woynyarvut21", '')
    schedule.every().day.at("08:45").do(send_message_func, "[Sun]GM", "47462575642@chatroom", '')
    schedule.every().day.at("22:45").do(send_message_func, "[Moon]GN", "47462575642@chatroom", '')


    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"程序运行时发生错误: {e}")
            logging.info("程序将在60秒后重试。")
            time.sleep(60)  # 发生错误时等待60秒后重试

def start_scheduler(send_message_func):
    """
    启动定时任务调度器
    """
    Thread(target=schedule_messages, args=(send_message_func,), name="PeriodicMessageThread", daemon=True).start()
