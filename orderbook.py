import ccxt

class OrderBookFetcher:
    """Fetches real-time order book data from MEXC"""
    
    def __init__(self, symbol='BTC/USDT'):
        # Initialize MEXC exchange connection (public, no API keys needed)
        self.exchange = ccxt.mexc({
            'enableRateLimit': True,  # Respect rate limits automatically
            'options': {'defaultType': 'spot'}  # Spot trading
        })
        self.symbol = symbol

    def get_best_bid_ask(self):
        """Returns the best bid (highest buy) and best ask (lowest sell) prices"""
        try:
            # Fetch order book with 5 levels depth
            orderbook = self.exchange.fetch_order_book(self.symbol, limit=5)
            best_bid = orderbook['bids'][0][0] if orderbook['bids'] else None
            best_ask = orderbook['asks'][0][0] if orderbook['asks'] else None
            return best_bid, best_ask
        except Exception as e:
            print(f"[OrderBook] Error: {e}")
            return None, None