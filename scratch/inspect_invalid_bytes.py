with open("templates/index.html", "rb") as f:
    data = f.read()

print("File size in bytes:", len(data))
# Inspect bytes around position 102280
start = max(0, 102280 - 100)
end = min(len(data), 102280 + 100)
print(f"Bytes from {start} to {end}:")
snippet = data[start:end]
print(snippet)

# Try decoding snippet and print the error location
try:
    snippet.decode('utf-8')
    print("Snippet decodes as UTF-8 successfully.")
except UnicodeDecodeError as e:
    print("Decode error:", e)
    # Print the specific byte causing it
    err_pos = start + e.start
    print(f"Error byte at file index {err_pos}: {data[err_pos]:#x} (index in snippet: {e.start})")
    print("Surrounding bytes:", data[err_pos-5:err_pos+6])
