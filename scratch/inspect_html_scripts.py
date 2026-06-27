import re

html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's find script blocks
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print("Found", len(scripts), "inline script blocks.")

for i, script in enumerate(scripts):
    print(f"\n--- Script {i+1} (Length: {len(script)}) ---")
    lines = script.splitlines()
    print("First 30 lines:")
    for line in lines[:30]:
        print(line.encode('ascii', 'ignore').decode())
    print("...")
    print("Last 20 lines:")
    for line in lines[-20:]:
        print(line.encode('ascii', 'ignore').decode())
