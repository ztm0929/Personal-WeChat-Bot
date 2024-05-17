import requests

url = (
    'https://api.coingecko.com/api/v3/simple/price'
    '?ids=bitcoin'
    '&vs_currencies=cny'
    '&include_last_updated_at=true'
    )

res = requests.get(url)

print(res.json())