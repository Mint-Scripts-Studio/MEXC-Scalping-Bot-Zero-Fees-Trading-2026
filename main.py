import time
from config import API_KEY, API_SECRET, SYMBOL, ORDER_AMOUNT, OFFSET_PCT, ORDER_REFRESH_SEC, CANCEL_OLD_ORDERS
from orderbook import OrderBookFetcher
from trader import ZeroFeeTrader

def main():
    print("🚀 MEXC Zero-Fee Scalper Started")
    print(f"Pair: {SYMBOL}, Volume: {ORDER_AMOUNT}, Refresh: {ORDER_REFRESH_SEC}s")
    print(f"Using zero maker fee strategy - placing orders INSIDE spread")
    
    # Initialize components
    fetcher = OrderBookFetcher(SYMBOL)
    trader = ZeroFeeTrader(API_KEY, API_SECRET, SYMBOL)

    # Main trading loop
    while True:
        # Get current market prices
        best_bid, best_ask = fetcher.get_best_bid_ask()

        # Skip if we couldn't get order book data
        if best_bid is None or best_ask is None:
            print("Waiting for order book data...")
            time.sleep(ORDER_REFRESH_SEC)
            continue

        # Cancel old orders if enabled
        if CANCEL_OLD_ORDERS:
            trader.cancel_all_orders()

        # Calculate maker order prices (inside the spread)
        # Buy price = bid + offset (higher than current best bid)
        buy_price = round(best_bid * (1 + OFFSET_PCT), 2)
        # Sell price = ask - offset (lower than current best ask)
        sell_price = round(best_ask * (1 - OFFSET_PCT), 2)

        print(f"\n📊 Best Bid: {best_bid} | Best Ask: {best_ask}")
        print(f"📈 Placing BUY limit @ {buy_price} (maker - zero fee)")
        print(f"📉 Placing SELL limit @ {sell_price} (maker - zero fee)")

        # Place both limit orders
        trader.place_limit_order('buy', buy_price, ORDER_AMOUNT)
        trader.place_limit_order('sell', sell_price, ORDER_AMOUNT)

        # Wait before next cycle
        time.sleep(ORDER_REFRESH_SEC)

if __name__ == "__main__":
    main()