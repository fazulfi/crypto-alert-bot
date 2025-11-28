# services/bybit.py
import requests

# coba endpoint v2 public; kalau tidak cocok, kita ganti
BYBIT_TICKER = 'https://api.bybit.com/v2/public/tickers'

def get_bybit_price(symbol: str):
    symbol = symbol.upper()
    try:
        r = requests.get(BYBIT_TICKER, params={'symbol': symbol}, timeout=8)
        r.raise_for_status()
        data = r.json()
        # data['result'] di v2 biasanya list
        if data.get('result'):
            tick = data['result'][0]
            price = tick.get('last_price') or tick.get('last') or tick.get('last_price')
            return float(price)
    except Exception:
        return None
