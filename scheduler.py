import schedule
import time
import logging
from threading import Thread
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def get_bitcoin_price():
    url = (
        'https://api.coingecko.com/api/v3/simple/price'
        '?ids=bitcoin'
        '&vs_currencies=cny'
        '&include_last_updated_at=true'
        )

    res = requests.get(url)
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

    res = requests.get(url, headers=headers).json()
    # 将返回的列表循环取出，拼接成字符串
    formatted_res = []
    for i, coin in enumerate(res):
        coin_info = f"#{i+1} {coin['name']} {coin['symbol'].upper()}\nCN¥{round(coin['current_price'], 2):,}\n1 Hours：{round(coin['price_change_percentage_1h_in_currency'], 2)}%\n24 Hours：{round(coin['price_change_percentage_24h_in_currency'], 2)}%\n7 Days：{round(coin['price_change_percentage_7d_in_currency'], 2)}%\n------"
        last_updated = coin['last_updated']
        last_updated = datetime.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
        last_updated = last_updated + datetime.timedelta(hours=8)
        last_updated = last_updated.strftime("%Y-%m-%d %H:%M:%S")
        formatted_res.append(coin_info)

    txt = f"""📈 Crypto市值排名：
币种-当前汇率-涨跌
{'\n'.join(formatted_res)}

🕒 更新时间：
{last_updated} UTC+8

📊 Data from CoinGecko"""
    return txt


def schedule_messages(send_message_func):
    """
    定时发送消息的函数
    """
    schedule.every().day.at("08:00").do(send_message_func, "这是定时发送的消息", "wxid_92woynyarvut21", '')
    schedule.every().day.at("04:07").do(send_message_func, get_coin_rank(), "wxid_92woynyarvut21", '')
    schedule.every().day.at("08:45").do(send_message_func, "[Sun]GM", os.getenv("闲聊区@编程小白社"), '')
    schedule.every().day.at("08:50").do(send_message_func, get_coin_rank(), os.getenv("闲聊区@编程小白社"), '')
    schedule.every().day.at("22:45").do(send_message_func, "[Moon]GN", os.getenv("闲聊区@编程小白社"), '')


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
