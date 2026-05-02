from nasdaq_source import get_cocoa_price
from fx import get_usdidr
from pricing import selling_price, price_change
from storage import load_data, save_data
from notifier import send_telegram
from insights import generate_insight
import datetime

data = load_data()

price = get_cocoa_price()
fx = get_usdidr()
diff = data.get("diff", 0)

today = datetime.datetime.utcnow().weekday()
# Monday = 0, Sunday = 6

# 🧠 Monday logic: no weekend change
if today == 0:
    delta_idr, delta_usd = 0, 0
else:
    if data["last_price"]:
        delta_idr, delta_usd = price_change(price, data["last_price"], fx)
    else:
        delta_idr, delta_usd = 0, 0

sell_price = selling_price(price, diff, fx)

message = f"""
📊 Cocoa Daily Update

Price: ${price:.2f}/MT
USD/IDR: {fx:.0f}

Selling Price:
IDR {sell_price:,.0f}/MT

Change:
IDR {delta_idr:,.0f}/MT ({delta_usd:+.2f} USD)

{generate_insight(delta_usd)}
"""

send_telegram(message)

save_data({
    "last_price": price,
    "diff": diff
})
