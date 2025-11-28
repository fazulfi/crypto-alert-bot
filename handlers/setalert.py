# handlers/setalert.py
from services.alerts_db import add_alert
from ui.messages import ALERT_SET

def command(update, context):
    if len(context.args) < 3:
        return update.message.reply_text('Usage: /setalert SYMBOL above|below PRICE')
    symbol = context.args[0].upper()
    direction = context.args[1].lower()
    try:
        price = float(context.args[2])
    except ValueError:
        return update.message.reply_text('Price harus angka')
    aid = add_alert(update.effective_chat.id, symbol, direction, price)
    update.message.reply_text(ALERT_SET.format(symbol=symbol, direction=direction, price=price, id=aid), parse_mode='HTML')
