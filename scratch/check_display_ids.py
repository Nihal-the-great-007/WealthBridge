with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
display_ids = ["val-house-price", "val-down-payment-pct", "val-loan-rate", "val-loan-tenure", "val-safe-emi-pct"]
for i in display_ids:
    print(f"ID '{i}':", i in html)
