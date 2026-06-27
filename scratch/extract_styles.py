import re

with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Find style block
styles = re.findall(r'<style>(.*?)</style>', html, re.DOTALL)
if styles:
    with open("scratch/index_style.css", "w", encoding="utf-8") as out:
        out.write(styles[0])
    print("Styles extracted to scratch/index_style.css. Length:", len(styles[0]))
else:
    print("No style block found.")
