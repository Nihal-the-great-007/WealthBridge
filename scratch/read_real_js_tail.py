with open("scratch/index_script_real.js", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print("Total lines in index_script_real.js:", len(lines))
print("\n--- Last 150 lines ---")
for i in range(max(0, len(lines) - 150), len(lines)):
    clean_l = lines[i].strip().encode("ascii", "ignore").decode("ascii")
    print(f"{i+1}: {clean_l}")
