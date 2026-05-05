import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')

# Фьючерсные настройки
SYMBOL = 'SOL/USDT:USDT'      # Формат фьючерсов MEXC
ORDER_AMOUNT = 1              # 1 КОНТРАКТ = 1 SOL (не 0.2!)
OFFSET_PCT = 0.0005           # 0.05% смещение
ORDER_REFRESH_SEC = 2
CANCEL_OLD_ORDERS = True

# Для фьючерсов: маржа (примерно 5-10 USDT на 1 контракт SOL)
# При цене SOL 85 USDT и плече 10x на 1 контракт нужно ~8.5 USDT маржи
LEVERAGE = 10                 # Плечо
