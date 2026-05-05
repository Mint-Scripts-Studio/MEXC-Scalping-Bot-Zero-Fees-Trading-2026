import time
from config import API_KEY, API_SECRET, SYMBOL, ORDER_AMOUNT, OFFSET_PCT, ORDER_REFRESH_SEC, CANCEL_OLD_ORDERS, LEVERAGE
from orderbook import OrderBookFetcher
from trader import ZeroFeeTrader

def main():
    print("🚀 MEXC FUTURES Scalper (Zero Fee - Maker)")
    print(f"Pair: {SYMBOL}, Contracts: {ORDER_AMOUNT}, Refresh: {ORDER_REFRESH_SEC}s")
    
    fetcher = OrderBookFetcher(SYMBOL)
    trader = ZeroFeeTrader(API_KEY, API_SECRET, SYMBOL)
    
    # Устанавливаем плечо
    try:
        trader.exchange.set_leverage(LEVERAGE, SYMBOL)
        print(f"✅ Leverage set to {LEVERAGE}x")
    except:
        print("⚠️ Could not set leverage (may already be set)")

    while True:
        best_bid, best_ask = fetcher.get_best_bid_ask()
        
        if best_bid is None or best_ask is None:
            print("Waiting for order book...")
            time.sleep(ORDER_REFRESH_SEC)
            continue
        
        if CANCEL_OLD_ORDERS:
            trader.cancel_all_orders()
        
        # Получаем текущую позицию
        side, size = trader.get_position()
        
        print(f"\n📊 Best Bid: {best_bid} | Best Ask: {best_ask}")
        print(f"📌 Current position: {side if side else 'none'} ({size} contracts)")
        
        # Рассчитываем цены
        buy_price = round(best_bid * (1 + OFFSET_PCT), 2)
        sell_price = round(best_ask * (1 - OFFSET_PCT), 2)
        
        # Стратегия: открываем позицию, если её нет
        if side is None:
            print(f"📈 Opening LONG with BUY limit @ {buy_price}")
            trader.place_limit_order('buy', buy_price, ORDER_AMOUNT)
        else:
            print(f"Position exists, waiting to close via opposite order...")
            # Бот не будет открывать вторую позицию
        
        time.sleep(ORDER_REFRESH_SEC)

if __name__ == "__main__":
    main()
