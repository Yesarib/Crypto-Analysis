from datetime import datetime

import requests
import json


def get_crypto_history():
    url = "https://openapiv1.coinstats.app/coins/bitcoin/charts?period=1y"
    headers = {"X-API-KEY": "yYqgPbsFqw504zxdgCFXPwXKvTNA8IVJ2jvvqCecrpY="}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    # Tarih bilgisini ekleyin
    for item in data:
        timestamp = item[0]
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        item.append(date)

    return data

