# handlers/alerts.py
from services.alerts_db import get_alerts_by_chat
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def command(update, context):
    chat_id = update.effective_chat.id
    rows = get_alerts_by_chat(chat_id)
    if not rows:
        return update.message.reply_text('Kamu tidak punya alert')
    lines = []
    buttons = []
    for r in rows:
        aid, symbol, direction, price, triggered, created = r
        status = '✅' if triggered else '⏳'
        lines.append(f"{status} {symbol} {direction} {price} (id={aid})")
        buttons.append([InlineKeyboardButton(f"Delete {aid}", callback_data=f"del:{aid}")])
    update.message.reply_text('\n'.join(lines), reply_markup=InlineKeyboardMarkup(buttons))
