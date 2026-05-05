import ccxt

class ZeroFeeTrader:
    def __init__(self, api_key, api_secret, symbol='SOL/USDT:USDT'):
        self.exchange = ccxt.mexc({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'  # <-- ФЬЮЧЕРСЫ
            }
        })
        self.symbol = symbol
        self.position_side = None  # 'long' или 'short'
        self.position_size = 0

    def cancel_all_orders(self):
        try:
            orders = self.exchange.fetch_open_orders(self.symbol)
            for order in orders:
                self.exchange.cancel_order(order['id'], self.symbol)
                print(f"[Cancel] Order {order['id']} cancelled")
        except Exception as e:
            print(f"[Cancel Error] {e}")

    def get_position(self):
        """Получить текущую позицию по фьючерсу"""
        try:
            positions = self.exchange.fetch_positions([self.symbol])
            for pos in positions:
                if pos['symbol'] == self.symbol:
                    self.position_size = float(pos['contracts'])
                    self.position_side = 'long' if float(pos['contracts']) > 0 else 'short' if float(pos['contracts']) < 0 else None
                    return self.position_side, abs(self.position_size)
            return None, 0
        except Exception as e:
            print(f"[Position Error] {e}")
            return None, 0

    def place_limit_order(self, side, price, amount):
        """
        side: 'buy' (лонг) или 'sell' (шорт)
        amount: количество КОНТРАКТОВ (на MEXC 1 контракт = 1 SOL)
        """
        try:
            # Для фьючерсов используем create_limit_order
            order = self.exchange.create_limit_order(
                symbol=self.symbol,
                side=side,
                amount=amount,
                price=price,
                params={'positionSide': 'LONG' if side == 'buy' else 'SHORT'}
            )
            print(f"[Success] {side.upper()} {amount} contracts {self.symbol} @ {price}")
            return order
        except Exception as e:
            print(f"[Order Error] {side} @ {price} -> {e}")
            return None

    def place_maker_orders(self, bid_price, ask_price, amount):
        """Выставляет только ОДИН ордер в зависимости от текущей позиции"""
        side, size = self.get_position()
        
        if side is None:
            # Нет позиции - можно открыть и лонг, и шорт? Нет, только одну
            print("📌 Нет позиции. Открываю LONG (покупку)")
            buy_price = round(bid_price * (1 + 0.0005), 2)
            self.place_limit_order('buy', buy_price, amount)
        elif side == 'long':
            # Есть лонг - можно поставить тейк-профит (sell)
            sell_price = round(ask_price * (1 - 0.0005), 2)
            print(f"📉 Есть LONG позиция {size} SOL. Выставляю SELL (тейк-профит)")
            self.place_limit_order('sell', sell_price, size)  # Продаём всю позицию
        elif side == 'short':
            # Есть шорт - можно закрыть buy
            buy_price = round(bid_price * (1 + 0.0005), 2)
            print(f"📈 Есть SHORT позиция {size} SOL. Выставляю BUY (закрытие)")
            self.place_limit_order('buy', buy_price, size)
