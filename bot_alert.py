# bot_alert.py
import os
import logging
import threading
import time
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handlers import start, price, setalert, alerts, callbacks
from services.alerts_db import init_db, get_pending_alerts, mark_triggered
from services.bybit import get_bybit_price
from ui.messages import ALERT_TEMPLATE

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '10'))

if not TOKEN:
    logger.error('TELEGRAM_TOKEN tidak diset di environment')
    raise SystemExit(1)

# init DB
init_db()

updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

# register handlers
dp.add_handler(CommandHandler('start', start.command))
dp.add_handler(CommandHandler('price', price.command))
dp.add_handler(CommandHandler('setalert', setalert.command))
dp.add_handler(CommandHandler('alerts', alerts.command))
dp.add_handler(CommandHandler('remove', callbacks.remove_command))
dp.add_handler(CallbackQueryHandler(callbacks.callback_query))

def alert_worker(bot):
    """Thread worker: cek DB, fetch price per symbol, kirim notif dan mark triggered"""
    while True:
        try:
            rows = get_pending_alerts()  # list of (id,chat_id,symbol,direction,price)
            if rows:
                # ambil semua symbol unik
                symbols = list({r[2] for r in rows})
                price_map = {}
                for s in symbols:
                    price_map[s] = get_bybit_price(s)
                    logger.info(f"Price fetch {s} -> {price_map[s]}")
                for aid, chat_id, symbol, direction, threshold in rows:
                    current = price_map.get(symbol)
                    logger.info(f"Check id={aid} sym={symbol} cur={current} dir={direction} thr={threshold}")
                    if current is None:
                        logger.info(f"Skip id={aid} karena price None")
                        continue
                    hit = (direction == 'above' and current >= threshold) or (direction == 'below' and current <= threshold)
                    if hit:
                        text = ALERT_TEMPLATE.format(
                            symbol=symbol,
                            direction=direction,
                            threshold=threshold,
                            price=f"{current:,.2f}",
                            timestamp=datetime.utcnow().isoformat() + " UTC"
                        )
                        try:
                            bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
                            logger.info(f"Sent alert id={aid} to {chat_id}")
                        except Exception as e:
                            logger.exception("Gagal kirim alert")
                        mark_triggered(aid)
            time.sleep(CHECK_INTERVAL)
        except Exception:
            logger.exception("Worker error")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    # start worker thread (daemon)
    worker = threading.Thread(target=alert_worker, args=(updater.bot,), daemon=True)
    worker.start()
    logger.info("Alert worker started")
    # start bot polling
    updater.start_polling()
    updater.idle()
