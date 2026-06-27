import re

with open("templates/index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Let's remove the script and style blocks
html_no_style = re.sub(r'<style>.*?</style>', '<!-- STYLE -->', html, flags=re.DOTALL)
html_no_js = re.sub(r'<script>.*?</script>', '<!-- SCRIPT -->', html_no_style, flags=re.DOTALL)

# Print the remaining html structure to a file
with open("scratch/structure.txt", "w", encoding="utf-8") as out:
    out.write(html_no_js)

print("HTML structure without JS and CSS written to scratch/structure.txt")
