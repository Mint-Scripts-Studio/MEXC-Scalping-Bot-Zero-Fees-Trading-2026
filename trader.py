import ccxt
import time

class ZeroFeeTrader:
    """Handles all trading operations on MEXC with zero maker fee strategy"""
    
    def __init__(self, api_key, api_secret, symbol='BTC/USDT'):
        # Initialize authenticated exchange connection
        self.exchange = ccxt.mexc({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        self.symbol = symbol

    def cancel_all_orders(self):
        """Cancel all open limit orders for the current symbol"""
        try:
            orders = self.exchange.fetch_open_orders(self.symbol)
            for order in orders:
                self.exchange.cancel_order(order['id'], self.symbol)
                print(f"[Cancel] Order {order['id']} cancelled")
            if orders:
                print(f"[Cancel] Cancelled {len(orders)} orders")
        except Exception as e:
            print(f"[Cancel Error] {e}")

    def place_limit_order(self, side, price, amount):
        """
        Place a single limit order
        side: 'buy' or 'sell'
        price: limit price
        amount: volume in base currency
        """
        try:
            order = self.exchange.create_limit_order(
                symbol=self.symbol,
                side=side,
                amount=amount,
                price=price
            )
            print(f"[Success] {side.upper()} {amount} {self.symbol} @ {price}")
            return order
        except Exception as e:
            print(f"[Order Error] {side} @ {price} -> {e}")
            return None

    def place_maker_orders(self, bid_price, ask_price, amount):
        """
        Place both buy and sell limit orders that act as makers (zero fee)
        Buy order is placed slightly ABOVE best bid
        Sell order is placed slightly BELOW best ask
        """
        # Buy limit order slightly above best bid (maker)
        buy_price = round(bid_price * (1 + 0.0001), 2)  # +0.01%
        # Sell limit order slightly below best ask (maker)
        sell_price = round(ask_price * (1 - 0.0001), 2)  # -0.01%

        self.place_limit_order('buy', buy_price, amount)
        self.place_limit_order('sell', sell_price, amount)