import ccxt

class OrderBookFetcher:
    def __init__(self, symbol='SOL/USDT:USDT'):  # Фьючерсный формат
        self.exchange = ccxt.mexc({
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}  # <-- МЕНЯЕМ НА FUTURE
        })
        self.symbol = symbol

    def get_best_bid_ask(self):
        try:
            orderbook = self.exchange.fetch_order_book(self.symbol, limit=5)
            best_bid = orderbook['bids'][0][0] if orderbook['bids'] else None
            best_ask = orderbook['asks'][0][0] if orderbook['asks'] else None
            return best_bid, best_ask
        except Exception as e:
            print(f"[OrderBook] Ошибка: {e}")
            return None, None
