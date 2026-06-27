with open("scratch/index_style.css", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "startup" in line.lower() or "loading-overlay" in line.lower():
        # Print the surrounding lines
        print(f"--- Line {i+1} ---")
        start = max(0, i - 5)
        end = min(len(lines), i + 15)
        for j in range(start, end):
            clean_l = lines[j].strip().encode("ascii", "ignore").decode("ascii")
            print(f"{j+1}: {clean_l}")
        print()
