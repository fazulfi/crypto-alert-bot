# ui/messages.py
ALERT_TEMPLATE = (
    "🚨 <b>ALERT</b>\n"
    "<b>{symbol}</b> sudah <i>{direction} {threshold}</i>\n"
    "Current: <code>{price}</code>\n"
    "<i>{timestamp}</i>"
)

START_TEXT = (
    "<b>Crypto Alert Bot</b>\n"
    "Perintah:\n"
    "<code>/price BTCUSDT</code>\n"
    "<code>/setalert BTCUSDT above 70000</code>\n"
    "<code>/alerts</code>\n"
    "<code>/remove ID</code>\n\n"
    "Kirim 1 perintah per pesan."
)

PRICE_TEMPLATE = "<b>{symbol}</b> price: <code>{price}</code>"

ALERT_SET = "✅ Alert diset: <b>{symbol}</b> {direction} <code>{price}</code> (id={id})"
