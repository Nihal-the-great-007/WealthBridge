with open("scratch/index_script_real.js", "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer("exportData", js, re.IGNORECASE)]
print("Found exportData in JS:", len(matches))
for idx in matches:
    print("  Snippet:", js[max(0, idx-50):min(len(js), idx+150)].strip().replace('\n', ' '))
