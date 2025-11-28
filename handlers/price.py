# handlers/price.py
from services.bybit import get_bybit_price
from ui.messages import PRICE_TEMPLATE
import html

def command(update, context):
    if not context.args:
        return update.message.reply_text('Usage: /price SYMBOL')
    symbol = context.args[0].upper()
    p = get_bybit_price(symbol)
    if p is None:
        update.message.reply_text(f'Gagal ambil harga untuk {symbol}')
    else:
        update.message.reply_text(PRICE_TEMPLATE.format(symbol=html.escape(symbol), price=f"{p:,.2f}"), parse_mode='HTML')
