import re

with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

print("File length:", len(html))

# Let's find some keywords
for kw in ["wecare", "model", "pension", "motto", "title", "header", "h1", "h2", "style"]:
    matches = [m.start() for m in re.finditer(kw, html, re.IGNORECASE)]
    print(f"Keyword '{kw}': {len(matches)} matches")

# Print first 200 lines to a file with ASCII-only characters so we can inspect it safely
ascii_html = html.encode("ascii", "ignore").decode("ascii")
lines = ascii_html.splitlines()
with open("scratch/index_head.html", "w") as out:
    out.write("\n".join(lines[:300]))
print("First 300 lines written to scratch/index_head.html")
