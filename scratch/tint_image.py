from PIL import Image
import os

src_path = r"C:\Users\sharv\.gemini\antigravity-ide\brain\dd61ad22-f202-4a0d-a052-8e0faef65181\media__1782588911663.jpg"
dest_path = r"templates\background-pattern.jpg"

if not os.path.exists(src_path):
    print("Source image not found at:", src_path)
    # Check if there is another image in the folder
    print("Files in brain folder:", os.listdir(os.path.dirname(src_path)))
    sys.exit(1)

# Open image
img = Image.open(src_path)
print(f"Image loaded. Format: {img.format}, Size: {img.size}, Mode: {img.mode}")

# We want to tint the green lines to a beautiful beige and make the white background a soft warm cream.
# Let's define the beige color for the lines and soft off-white for the background.
# Line color (Beige): #DECDB3 (RGB: 222, 205, 179)
# Background color (Soft Warm Off-white): #FAF8F5 (RGB: 250, 248, 245)

target_line_color = (222, 205, 179)
target_bg_color = (250, 248, 245)

# Convert to RGB mode if not already
if img.mode != 'RGB':
    img = img.convert('RGB')

# Load pixel data
pixels = img.load()
width, height = img.size

# Process pixels
for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]
        # Calculate lightness/luminance
        L = 0.299 * r + 0.587 * g + 0.114 * b
        
        # Normalized lightness t (0 to 1)
        t = L / 255.0
        
        # Interpolate between target_line_color and target_bg_color
        new_r = int(target_line_color[0] + (target_bg_color[0] - target_line_color[0]) * t)
        new_g = int(target_line_color[1] + (target_bg_color[1] - target_line_color[1]) * t)
        new_b = int(target_line_color[2] + (target_bg_color[2] - target_line_color[2]) * t)
        
        # Clamp values
        new_r = max(0, min(255, new_r))
        new_g = max(0, min(255, new_g))
        new_b = max(0, min(255, new_b))
        
        pixels[x, y] = (new_r, new_g, new_b)

# Save image
img.save(dest_path, "JPEG", quality=90)
print("Successfully tinted image and saved to", dest_path)
