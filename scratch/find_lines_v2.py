html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

targets = [
    ('id="wc-wecare"', 'wecare card'),
    ('id="ri-wecare"', 'ri-wecare row'),
    ('document.getElementById(\'wc-wecare\')', 'JS wc-wecare update'),
    ('document.getElementById(\'ri-wecare\')', 'JS ri-wecare update')
]

for target, desc in targets:
    found = False
    for idx, line in enumerate(lines):
        if target in line:
            print(f"Found '{desc}' at line {idx+1}: {line.strip()[:100]}")
            found = True
    if not found:
        print(f"NOT FOUND: '{desc}' with target '{target}'")
