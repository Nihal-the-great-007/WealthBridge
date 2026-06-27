import re

with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Let's find the inline script
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if scripts:
    script = scripts[0]
    matches = [m.start() for m in re.finditer("startup-screen", script, re.IGNORECASE)]
    print(f"Found {len(matches)} matches in index.html script block")
    for idx in matches:
        print("--- Match ---")
        start = max(0, idx - 400)
        end = min(len(script), idx + 600)
        snippet = script[start:end].encode("ascii", "ignore").decode("ascii")
        print(snippet)
else:
    print("No inline script block found in index.html")
