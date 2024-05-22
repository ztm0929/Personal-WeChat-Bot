import schedule
import time
import logging
from threading import Thread
import requests
import datetime
from dotenv import load_dotenv
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

# 设置重试策略
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

def get_bitcoin_price():
    url = (
        'https://api.coingecko.com/api/v3/simple/price'
        '?ids=bitcoin'
        '&vs_currencies=cny'
        '&include_last_updated_at=true'
    )

    res = http.get(url)
    return res.text

def get_coin_rank():
    url = (
        'https://api.coingecko.com/api/v3/coins/markets'
        '?vs_currency=cny'
        '&order=market_cap_desc'
        '&per_page=5'
        '&page=1'
        '&locale=zh'
        '&price_change_percentage=1h%2C24h%2C7d'
    )
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }

    res = http.get(url, headers=headers).json()
    
    formatted_res = []
    for i, coin in enumerate(res):
        coin_info = (
            f"#{i+1} {coin['name']} {coin['symbol'].upper()}\n"
            f"CN¥{round(coin['current_price'], 2):,}\n"
            f"1 Hours：{round(coin['price_change_percentage_1h_in_currency'], 2)}%\n"
            f"24 Hours：{round(coin['price_change_percentage_24h_in_currency'], 2)}%\n"
            f"7 Days：{round(coin['price_change_percentage_7d_in_currency'], 2)}%\n"
            f"------"
        )
        last_updated = datetime.datetime.strptime(coin['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)
        formatted_res.append(coin_info)

    last_updated_str = last_updated.strftime("%Y-%m-%d %H:%M:%S")
    txt = (
        f"📈 Crypto市值排名：\n"
        f"币种-当前汇率-涨跌\n"
        f"{'\n'.join(formatted_res)}\n\n"
        f"🕒 更新时间：\n"
        f"{last_updated_str} UTC+8\n\n"
        f"📊 Data from CoinGecko"
    )
    return txt

def schedule_messages(send_message_func):
    """
    定时发送消息的函数
    """
    times = ["04:20", "05:00", "08:45", "08:50", "22:45"]
    messages = [
        (get_coin_rank, "wxid_92woynyarvut21", ''),
        (get_coin_rank, "wxid_92woynyarvut21", ''),
        ("[Sun]GM", os.getenv("闲聊区@编程小白社"), ''),
        (get_coin_rank, os.getenv("闲聊区@编程小白社"), ''),
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
