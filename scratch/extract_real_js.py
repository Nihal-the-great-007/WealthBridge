import re

with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if scripts:
    with open("scratch/index_script_real.js", "w", encoding="utf-8") as out:
        out.write(scripts[0])
    print("Script extracted to scratch/index_script_real.js. Length:", len(scripts[0]))
else:
    print("No script block found")
