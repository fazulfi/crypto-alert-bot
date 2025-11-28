# handlers/start.py
from ui.messages import START_TEXT

def command(update, context):
    update.message.reply_text(START_TEXT, parse_mode='HTML')
