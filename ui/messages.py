# ui/messages.py
# Message templates centralised.
# Pastikan handlers memakai .format(...) sesuai placeholder di bawah.

ALERT_TEMPLATE = (
    "🚨 <b>ALERT</b>\n"
    "<b>{symbol}</b> sudah <i>{direction} {threshold}</i>\n"
    "Current: <code>{price}</code>\n"
    "<i>{timestamp}</i>"
)

# Backwards-compatible alias (some handlers used ALERT_TRIGGER_MESSAGE)
ALERT_TRIGGER_MESSAGE = ALERT_TEMPLATE
ALERT_TRIGGER = ALERT_TEMPLATE

START_TEXT = (
    "<b>Crypto Alert Bot</b>\n"
    "Perintah:\n"
    "<code>/price BTCUSDT</code>\n"
    "<code>/setalert BTCUSDT above 70000</code>\n"
    "<code>/alerts</code>\n"
    "<code>/remove ID</code>\n\n"
    "Kirim 1 perintah per pesan."
)

# handy alias names used in handlers
start_message = START_TEXT
START = START_TEXT

# price template — handlers might call PRICE_TEMPLATE.format(symbol=..., price=...)
PRICE_TEMPLATE = "<b>{symbol}</b> price: <code>{price}</code>"
PRICE_MESSAGE = PRICE_TEMPLATE
price_message = PRICE_TEMPLATE

# alert set acknowledgement
ALERT_SET = "✅ Alert diset: <b>{symbol}</b> {direction} <code>{price}</code> (id={id})"
ALERT_SET_MESSAGE = ALERT_SET
alert_set_message = ALERT_SET

# usage/help snippets
USAGE_PRICE = "Usage: /price SYMBOL"
USAGE_SETA = "Usage: /setalert SYMBOL above|below PRICE"
USAGE_SETALERT = USAGE_SETA

# no-alerts message
NO_ALERTS_MESSAGE = "Kamu tidak punya alert."
no_alerts_message = NO_ALERTS_MESSAGE

# small helper to safely coerce templates if someone imports non-string later
def _s(x):
    return x if isinstance(x, str) else str(x)

# Re-assign cleaned strings back (this avoids accidental non-string at import time)
ALERT_TEMPLATE = _s(ALERT_TEMPLATE)
ALERT_TRIGGER_MESSAGE = _s(ALERT_TRIGGER_MESSAGE)
START_TEXT = _s(START_TEXT)
PRICE_TEMPLATE = _s(PRICE_TEMPLATE)
ALERT_SET = _s(ALERT_SET)

# Exports (names listed so you can introspect)
__all__ = [
    "ALERT_TEMPLATE", "ALERT_TRIGGER_MESSAGE", "START_TEXT",
    "PRICE_TEMPLATE", "ALERT_SET", "USAGE_PRICE", "USAGE_SETALERT",
    "NO_ALERTS_MESSAGE"
]
