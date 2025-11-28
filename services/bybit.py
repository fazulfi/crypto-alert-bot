# services/bybit.py
import requests

def get_bybit_price(symbol):
    symbol = symbol.upper()
    try:
        r = requests.get(
            "https://api.bybit.com/v5/market/tickers",
            params={"category": "linear", "symbol": symbol},
            timeout=8
        )
        if r.status_code != 200:
            return None

        j = r.json()
        if j.get("retCode") != 0:
            return None

        lst = j.get("result", {}).get("list", [])
        if not lst:
            return None

        p = lst[0].get("lastPrice") or lst[0].get("last_price") or lst[0].get("last")
        if p is None:
            return None

        return float(p)

    except Exception:
        return None
