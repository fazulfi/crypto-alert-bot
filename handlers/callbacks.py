# handlers/callbacks.py
from services.alerts_db import delete_alert
from telegram.ext import CallbackContext

def callback_query(update, context: CallbackContext):
    q = update.callback_query
    if not q.data:
        return
    if q.data.startswith('del:'):
        aid = int(q.data.split(':',1)[1])
        delete_alert(aid, q.message.chat.id)
        q.answer(text=f'Alert {aid} dihapus')
        q.edit_message_text(f'Alert {aid} dihapus')

def remove_command(update, context):
    if not context.args:
        return update.message.reply_text('Usage: /remove ID')
    try:
        aid = int(context.args[0])
    except ValueError:
        return update.message.reply_text('ID harus angka')
    delete_alert(aid, update.effective_chat.id)
    update.message.reply_text(f'Alert {aid} dihapus')
