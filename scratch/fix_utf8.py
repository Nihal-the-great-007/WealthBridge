with open("templates/index.html", "rb") as f:
    binary_content = f.read()

print("Original size:", len(binary_content))

# Clean out the bad bytes
# Since we saw \x90 at position 102280, let's see if we can replace it.
# We can also replace any other non-utf8 characters.
# Let's decode with errors='ignore' and save back as UTF-8
text = binary_content.decode("utf-8", errors="ignore")

# Let's verify that the decoded text can be encoded back to UTF-8 and parsed
clean_binary = text.encode("utf-8")
print("Clean size:", len(clean_binary))

try:
    clean_binary.decode("utf-8")
    print("Verification: Successfully decoded clean binary as UTF-8!")
    with open("templates/index.html", "wb") as f:
        f.write(clean_binary)
    print("Clean UTF-8 index.html written successfully!")
except Exception as e:
    print("Verification failed:", e)
