import urllib.parse
import urllib.request
from django.conf import settings

def send_order_to_telegram(order):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return False, "Telegram sozlanmagan"

    lines = [
        f"🛒 FreshMart yangi buyurtma #{order.id}",
        f"👤 {order.full_name}",
        f"📞 {order.phone}",
        f"📍 {order.address}",
        f"💳 {order.payment_method}",
        f"💰 {order.total_price} so'm",
    ]
    for item in order.items.all():
        lines.append(f"• {item.product_name} x {item.quantity} — {item.price} so'm")
    if order.notes:
        lines.append(f"📝 {order.notes}")

    text = "\n".join(lines)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({'chat_id': chat_id, 'text': text}).encode('utf-8')
    try:
        with urllib.request.urlopen(url, data=data, timeout=10) as response:
            return response.status == 200, "ok"
    except Exception as e:
        return False, str(e)
