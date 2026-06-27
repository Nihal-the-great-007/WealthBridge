with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer("loading-overlay", html, re.IGNORECASE)]
print("Found loading-overlay in HTML:", len(matches))
for idx in matches:
    snippet = html[max(0, idx-50):min(len(html), idx+150)].strip().replace('\n', ' ')
    print("  Snippet:", snippet.encode("ascii", "ignore").decode("ascii"))
