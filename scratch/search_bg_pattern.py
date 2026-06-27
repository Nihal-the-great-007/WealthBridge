with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer("background-pattern.jpg", html, re.IGNORECASE)]
print("Found matches in index.html:", len(matches))
for idx in matches:
    print("  Snippet:", html[max(0, idx-100):min(len(html), idx+150)].strip().replace('\n', ' '))
