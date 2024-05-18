import json

import requests

from models import coinData as coin

baseUrl = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=cny&include_last_updated_at=true"


def getCoinData():
    res = requests.get(baseUrl)
    coinJsonData = res.json()

    coinData = json.loads(coinJsonData)
    return coin.CoinData(coinData["bitcoin"]["cny"], coinData["bitcoin"]["last_updated_at"])

# Todo: 1:未进行任何错误处理
#  2.未进行时间解析（将UTC时间解析为本地时间）
