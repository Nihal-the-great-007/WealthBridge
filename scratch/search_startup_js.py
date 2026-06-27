with open("scratch/inline_script.js", "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer("startup-screen", js, re.IGNORECASE)]
print("Found matches in inline_script.js:", len(matches))
for idx in matches:
    print(js[max(0, idx-100):min(len(js), idx+300)])
