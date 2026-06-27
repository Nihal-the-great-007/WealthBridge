with open("scratch/index_script_real.js", "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer("exportData", js, re.IGNORECASE)]
if matches:
    idx = matches[0]
    print("--- exportData implementation (tail 2) ---")
    print(js[idx+2500:idx+4500].encode("ascii", "ignore").decode("ascii"))
else:
    print("Not found")
