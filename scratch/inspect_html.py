import re

html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

print("File loaded. Length:", len(html))

# Find form fields / inputs
inputs = re.findall(r'<input[^>]*id="([^"]+)"[^>]*>', html)
print("\n--- Inputs ---")
for inp in sorted(list(set(inputs))):
    print(inp)

# Find select fields
selects = re.findall(r'<select[^>]*id="([^"]+)"[^>]*>', html)
print("\n--- Selects ---")
for sel in sorted(list(set(selects))):
    print(sel)

# Find charts
charts = re.findall(r'<canvas[^>]*id="([^"]+)"[^>]*>', html)
print("\n--- Canvas / Charts ---")
for chart in sorted(list(set(charts))):
    print(chart)

# Find tabs
tabs = re.findall(r'<[^>]*class="[^"]*tab[^"]*"[^>]*id="([^"]+)"[^>]*>', html)
print("\n--- Tabs ---")
for tab in sorted(list(set(tabs))):
    print(tab)

# Find scripts
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("\n--- Script Srcs ---")
for script in scripts:
    print(script)

# Inline script endpoints (e.g. fetch urls)
fetches = re.findall(r'fetch\([\'"]([^\'"]+)[\'"]', html)
print("\n--- Fetches ---")
for fetch in sorted(list(set(fetches))):
    print(fetch)
