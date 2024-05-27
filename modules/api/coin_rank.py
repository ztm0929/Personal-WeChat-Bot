import requests
import datetime
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class CoinRank:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.http = self._init_http_session()
    
    def _init_http_session(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        return http
    
    def get_coin_rank(self):
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
            "x-cg-demo-api-key": self.api_key
        }

        res = self.http.get(url, headers=headers).json()
        
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
            f"📊 Data from CoinGecko\n"
            f"coingecko.com/zh/api"
        )
        return txt
