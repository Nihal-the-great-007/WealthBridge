with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

import re
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print("Number of inline scripts:", len(scripts))
for i, script in enumerate(scripts):
    matches = [m.start() for m in re.finditer("startup-screen", script, re.IGNORECASE)]
    print(f"Script {i+1} has {len(matches)} occurrences of 'startup-screen'")
    for idx in matches:
        print("  Snippet:", script[max(0, idx-50):min(len(script), idx+150)].strip().replace('\n', ' '))
