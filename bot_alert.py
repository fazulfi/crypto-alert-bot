import os
import sqlite3
import requests
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

# Load environment
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))

# SQLite setup
DB_FILE = "alerts.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT,
    symbol TEXT,
    direction TEXT,
    price REAL,
    triggered INTEGER DEFAULT 0,
    created_at TEXT
)
""")
conn.commit()

# === Fetch Price From Bybit ===
def get_bybit_price(symbol: str):
    try:
        url = "https://api.bybit.com/v5/market/tickers"
        params = {"category": "spot", "symbol": symbol}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if data.get("retCode") != 0:
            return None

        price = float(data["result"]["list"][0]["lastPrice"])
        return price

    except:
        return None


# === Telegram Commands ===

def start(update, context):
    update.message.reply_text(
        "Bot aktif!\n"
        "Perintah:\n"
        "/price BTCUSDT\n"
        "/setalert BTCUSDT above 60000\n"
        "/alerts\n"
        "/remove 1"
    )

def price_cmd(update, context):
    if len(context.args) < 1:
        return update.message.reply_text("Usage: /price SYMBOL")

    symbol = context.args[0].upper()
    p = get_bybit_price(symbol)

    if p is None:
        update.message.reply_text(f"Gagal ambil harga untuk {symbol}")
    else:
        update.message.reply_text(f"{symbol} price: {p}")

def setalert(update, context):
    if len(context.args) < 3:
        return update.message.reply_text("Usage: /setalert SYMBOL above|below PRICE")

    symbol = context.args[0].upper()
    direction = context.args[1].lower()
    price = float(context.args[2])
    chat_id = str(update.effective_chat.id)
    created = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO alerts (chat_id, symbol, direction, price, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (chat_id, symbol, direction, price, created))
    conn.commit()

    update.message.reply_text(f"Alert diset: {symbol} {direction} {price}")

def alerts(update, context):
    chat_id = str(update.effective_chat.id)
    cur.execute("SELECT id, symbol, direction, price, triggered FROM alerts WHERE chat_id=?", (chat_id,))
    rows = cur.fetchall()

    if not rows:
        return update.message.reply_text("Kamu tidak punya alert.")

    msg = "\n".join(
        f"id={r[0]} | {r[1]} {r[2]} {r[3]} | triggered={r[4]}"
        for r in rows
    )
    update.message.reply_text(msg)

def remove(update, context):
    if len(context.args) < 1:
        return update.message.reply_text("Usage: /remove ID")

    aid = int(context.args[0])
    chat_id = str(update.effective_chat.id)

    cur.execute("DELETE FROM alerts WHERE id=? AND chat_id=?", (aid, chat_id))
    conn.commit()

    update.message.reply_text(f"Alert {aid} dihapus.")


# === ALERT WORKER (THREAD) ===
def alert_worker(bot):
    while True:
        cur.execute("SELECT id, chat_id, symbol, direction, price FROM alerts WHERE triggered=0")
        rows = cur.fetchall()

        if rows:
            symbols = list(set([r[2] for r in rows]))
            price_map = {s: get_bybit_price(s) for s in symbols}

            for row in rows:
                aid, chat_id, symbol, direction, threshold = row
                current = price_map.get(symbol)

                if current is None:
                    continue

                hit = (
                    (direction == "above" and current >= threshold) or
                    (direction == "below" and current <= threshold)
                )

                if hit:
                    text = (
                        f"ALERT!\n"
                        f"{symbol} sudah {direction} {threshold}\n"
                        f"Current price: {current}"
                    )
                    bot.send_message(chat_id=chat_id, text=text)

                    cur.execute("UPDATE alerts SET triggered=1 WHERE id=?", (aid,))
                    conn.commit()

        time.sleep(CHECK_INTERVAL)


# === MAIN APP ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", price_cmd))
    dp.add_handler(CommandHandler("setalert", setalert))
    dp.add_handler(CommandHandler("alerts", alerts))
    dp.add_handler(CommandHandler("remove", remove))

    # Start alert worker thread
    worker = threading.Thread(target=alert_worker, args=(updater.bot,), daemon=True)
    worker.start()

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
