import re

with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if scripts:
    script = scripts[0]
    # Let's search for DOMContentLoaded and print lines around it
    matches = [m.start() for m in re.finditer("DOMContentLoaded", script, re.IGNORECASE)]
    print(f"Found {len(matches)} DOMContentLoaded matches")
    for idx in matches:
        print("--- Match ---")
        start = max(0, idx - 100)
        end = min(len(script), idx + 2000)
        snippet = script[start:end].encode("ascii", "ignore").decode("ascii")
        print(snippet)
else:
    print("No script block found")
