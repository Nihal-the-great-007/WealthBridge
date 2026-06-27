import re

html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if scripts:
    with open("scratch/inline_script.js", "w", encoding="utf-8") as f:
        f.write(scripts[0])
    print("Script extracted to scratch/inline_script.js. Length:", len(scripts[0]))
else:
    print("No inline script block found.")
