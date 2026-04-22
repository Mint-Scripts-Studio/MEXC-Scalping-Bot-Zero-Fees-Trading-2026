import os
from dotenv import load_dotenv

load_dotenv()

# API keys (get from .env file)
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')

# Bot settings
SYMBOL = 'BTC/USTS'          # Trading pair (BTC/USDT, ETH/USDT, etc.)
ORDER_AMOUNT = 0.001         # Order volume in base currency (min ~0.001 BTC)
OFFSET_PCT = 0.0005          # 0.05% offset from best bid/ask
ORDER_REFRESH_SEC = 2        # How often to refresh orders (seconds)
CANCEL_OLD_ORDERS = True     # Cancel old limit orders before placing new ones