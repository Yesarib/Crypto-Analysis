from binance.client import Client
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

def get_binance_api():
    binance_api_key = os.getenv("BINANCE_API_KEY")
    binance_api_secret = os.getenv("BINANCE_API_SECRET")
    client = Client(binance_api_key,binance_api_secret)

    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_1DAY  # Günlük fiyat verileri için

    # Başlangıç ve bitiş zamanını belirtin
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2024, 4, 17)

    # Geçmiş fiyat verilerini alın
    klines = client.get_historical_klines(symbol, interval, start_date.strftime("%d %b, %Y"),
                                          end_date.strftime("%d %b, %Y"))

    # Verileri içeren bir dizi oluşturun
    data = []
    for kline in klines:
        data.append({
            'timestamp': kline[0],
            'open': kline[1],
            'high': kline[2],
            'low': kline[3],
            'close': kline[4],
            'volume': kline[5],
            'quote_asset_volume': kline[7],
            'number_of_trades': kline[8],
        })

    return data
