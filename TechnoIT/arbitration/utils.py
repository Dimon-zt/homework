import threading
import time
import requests
from main.models import Exchanges, TradingPair, PriceData

# Обновление котировок через API
def update_prices():
    exchanges = Exchanges.objects.all()
    for exchange in exchanges:
        trading_pairs = TradingPair.objects.filter(exchanges_id=exchange)
        for pair in trading_pairs:
            # Пример вызова API
            response = requests.get(f"{exchange.api_url}/ticker?pair={pair.pair}")
            if response.status_code == 200:
                data = response.json()
                PriceData.objects.create(
                    exchanges_id=exchange,
                    pair_id=pair,
                    price_ask=data.get("ask"),
                    price_bid=data.get("bid"),
                    volume_24h=data.get("volume_24h"),
                    timestamp=data.get("timestamp"),
                )

# Функция для многопоточной обработки
def start_price_updating(interval):
    def worker():
        while True:
            update_prices()
            time.sleep(interval)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
