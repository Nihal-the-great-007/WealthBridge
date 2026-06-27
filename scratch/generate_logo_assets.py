"""
Generate all WealthBridge logo/favicon assets and update the app.
- Creates a crisp SVG logo (vector, scalable, for <svg> embedding and /logo.svg route)
- Converts the generated PNG logo to favicon.ico (multi-size: 16x16, 32x32, 48x48)
- Copies/resizes the logo PNG for all PWA icon sizes
- Copies the OG image to templates/
- Patches index.html with favicon link, SVG logo in topbar, OG meta tags
- Patches api/index.py with new routes for /favicon.ico, /logo.svg, /og-image.png
"""
from PIL import Image
import shutil, os

BASE       = r"c:\Users\sharv\Documents\MarshCase1\MarshCase1"
TEMPLATES  = os.path.join(BASE, "templates")
ARTIFACTS  = r"C:\Users\sharv\.gemini\antigravity-ide\brain\dd61ad22-f202-4a0d-a052-8e0faef65181"

LOGO_SRC   = os.path.join(ARTIFACTS, "wealthbridge_logo_icon_1782591293792.png")
OG_SRC     = os.path.join(ARTIFACTS, "wealthbridge_og_image_1782591310949.png")

# ─────────────────────────────────────────────────────────────────
# 1. GENERATE SVG LOGO (pure vector, embedded in HTML)
# ─────────────────────────────────────────────────────────────────
svg_logo = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="wb-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="#00b4db"/>
      <stop offset="100%" stop-color="#0083B0"/>
    </linearGradient>
  </defs>
  <!-- Rounded background square -->
  <rect width="64" height="64" rx="14" fill="url(#wb-grad)" opacity="0.15"/>
  <!-- Bridge arch left -->
  <path d="M8 44 Q16 20 28 24 Q20 24 24 44" stroke="url(#wb-grad)" stroke-width="3.5"
        stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <!-- Bridge arch right -->
  <path d="M40 44 Q44 20 56 44" stroke="url(#wb-grad)" stroke-width="3.5"
        stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <!-- Centre valley -->
  <path d="M24 44 Q32 28 40 44" stroke="url(#wb-grad)" stroke-width="3.5"
        stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <!-- Road / base line -->
  <line x1="6" y1="44" x2="58" y2="44" stroke="url(#wb-grad)" stroke-width="3"
        stroke-linecap="round"/>
  <!-- Cable lines left arch -->
  <line x1="16" y1="44" x2="18" y2="34" stroke="url(#wb-grad)" stroke-width="1.2" opacity="0.7"/>
  <line x1="22" y1="44" x2="23" y2="28" stroke="url(#wb-grad)" stroke-width="1.2" opacity="0.7"/>
  <!-- Cable lines right arch -->
  <line x1="42" y1="44" x2="43" y2="28" stroke="url(#wb-grad)" stroke-width="1.2" opacity="0.7"/>
  <line x1="48" y1="44" x2="50" y2="34" stroke="url(#wb-grad)" stroke-width="1.2" opacity="0.7"/>
</svg>'''

svg_path = os.path.join(TEMPLATES, "logo.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_logo)
print(f"Generated: logo.svg")

# ─────────────────────────────────────────────────────────────────
# 2. GENERATE favicon.ico (16, 32, 48 px multi-size)
# ─────────────────────────────────────────────────────────────────
logo_img = Image.open(LOGO_SRC).convert("RGBA")
ico_path = os.path.join(TEMPLATES, "favicon.ico")
sizes = [(16,16), (32,32), (48,48)]
icons = [logo_img.resize(sz, Image.LANCZOS) for sz in sizes]
icons[0].save(ico_path, format="ICO", sizes=sizes, append_images=icons[1:])
print(f"Generated: favicon.ico (16x16, 32x32, 48x48)")

# ─────────────────────────────────────────────────────────────────
# 3. REGENERATE PWA icons from the new logo image
# ─────────────────────────────────────────────────────────────────
for sz, name in [(192,"icon-192.png"), (512,"icon-512.png"), (180,"apple-touch-icon.png")]:
    out = logo_img.resize((sz, sz), Image.LANCZOS)
    # Add rounded corners mask
    from PIL import ImageDraw
    mask = Image.new("L", (sz, sz), 0)
    r = sz // 5
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sz-1, sz-1], radius=r, fill=255)
    result = Image.new("RGBA", (sz, sz), (0,0,0,0))
    result.paste(out, mask=mask)
    result.save(os.path.join(TEMPLATES, name), "PNG")
    print(f"Generated: {name} ({sz}x{sz})")

# ─────────────────────────────────────────────────────────────────
# 4. COPY OG image to templates
# ─────────────────────────────────────────────────────────────────
og_dest = os.path.join(TEMPLATES, "og-image.png")
shutil.copy2(OG_SRC, og_dest)
print(f"Copied: og-image.png to templates/")

# ─────────────────────────────────────────────────────────────────
# 5. PATCH index.html:
#    a) Replace brand-icon div with SVG logo
#    b) Add favicon + OG meta tags to <head>
#    c) Update manifest icons reference
# ─────────────────────────────────────────────────────────────────
HTML_PATH = os.path.join(TEMPLATES, "index.html")
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 5a: Replace PWA head tags section with favicon + OG tags
old_pwa_head = """  <!-- PWA Install Support -->
  <link rel="manifest" href="/manifest.json" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="apple-mobile-web-app-title" content="WealthBridge" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="theme-color" content="#0083B0" />
  <meta name="msapplication-TileColor" content="#0083B0" />"""

new_pwa_head = """  <!-- Favicon & App Icons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/svg+xml" href="/logo.svg" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <!-- PWA Install Support -->
  <link rel="manifest" href="/manifest.json" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="apple-mobile-web-app-title" content="WealthBridge" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="theme-color" content="#0083B0" />
  <meta name="msapplication-TileColor" content="#0083B0" />
  <meta name="msapplication-TileImage" content="/icon-144.png" />
  <!-- Open Graph / Social / Google Search Preview -->
  <meta property="og:type"        content="website" />
  <meta property="og:url"         content="http://127.0.0.1:8000/" />
  <meta property="og:title"       content="WealthBridge — Premium Retirement Planner" />
  <meta property="og:description" content="Bridging Today's Income with Tomorrow's Retirement. Interactive Monte Carlo retirement corpus projections with EPF, NPS, ELSS, WeCare analysis." />
  <meta property="og:image"       content="/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt"   content="WealthBridge Dashboard Preview" />
  <meta property="og:site_name"   content="WealthBridge" />
  <!-- Twitter Card -->
  <meta name="twitter:card"        content="summary_large_image" />
  <meta name="twitter:title"       content="WealthBridge — Premium Retirement Planner" />
  <meta name="twitter:description" content="Bridging Today's Income with Tomorrow's Retirement." />
  <meta name="twitter:image"       content="/og-image.png" />"""

if old_pwa_head in html:
    html = html.replace(old_pwa_head, new_pwa_head)
    print("Updated: <head> favicon + OG meta tags")
else:
    print("WARNING: Could not find PWA head block to replace")

# 5b: Replace the emoji brand-icon with the SVG logo
old_brand_icon = """      <div class="brand-icon">💎</div>"""
new_brand_icon = """      <div class="brand-icon" style="background:none;border:none;box-shadow:none;padding:0;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" width="42" height="42" aria-label="WealthBridge Logo">
          <defs>
            <linearGradient id="hdr-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%"   stop-color="#00f2fe"/>
              <stop offset="100%" stop-color="#0083B0"/>
            </linearGradient>
          </defs>
          <rect width="64" height="64" rx="14" fill="url(#hdr-grad)" opacity="0.12"/>
          <path d="M8 44 Q16 20 28 24 Q20 24 24 44" stroke="url(#hdr-grad)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          <path d="M40 44 Q44 20 56 44" stroke="url(#hdr-grad)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          <path d="M24 44 Q32 28 40 44" stroke="url(#hdr-grad)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          <line x1="6" y1="44" x2="58" y2="44" stroke="url(#hdr-grad)" stroke-width="3" stroke-linecap="round"/>
          <line x1="16" y1="44" x2="18" y2="34" stroke="url(#hdr-grad)" stroke-width="1.2" opacity="0.75"/>
          <line x1="22" y1="44" x2="23" y2="28" stroke="url(#hdr-grad)" stroke-width="1.2" opacity="0.75"/>
          <line x1="42" y1="44" x2="43" y2="28" stroke="url(#hdr-grad)" stroke-width="1.2" opacity="0.75"/>
          <line x1="48" y1="44" x2="50" y2="34" stroke="url(#hdr-grad)" stroke-width="1.2" opacity="0.75"/>
        </svg>
      </div>"""

if old_brand_icon in html:
    html = html.replace(old_brand_icon, new_brand_icon, 1)
    print("Updated: topbar brand icon with inline SVG logo")
else:
    print("WARNING: Could not find brand-icon div to replace")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Saved: index.html")

# ─────────────────────────────────────────────────────────────────
# 6. PATCH api/index.py with new routes
# ─────────────────────────────────────────────────────────────────
API_PATH = os.path.join(BASE, "api", "index.py")
with open(API_PATH, "r", encoding="utf-8") as f:
    api = f.read()

new_routes = """
# -- Route: Favicon .ico -------------------------------------------------------
@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    \"\"\"Serve browser favicon.ico (multi-size: 16/32/48).\"\"\"\
    p = BASE_DIR / "templates" / "favicon.ico"
    if not p.exists():
        raise HTTPException(status_code=404, detail="favicon.ico not found")
    return FileResponse(p, media_type="image/x-icon")


# -- Route: SVG Logo -----------------------------------------------------------
@app.get("/logo.svg", include_in_schema=False)
async def get_logo_svg():
    \"\"\"Serve the SVG vector logo for browser tab, header, and embeds.\"\"\"\
    p = BASE_DIR / "templates" / "logo.svg"
    if not p.exists():
        raise HTTPException(status_code=404, detail="logo.svg not found")
    return FileResponse(p, media_type="image/svg+xml",
                        headers={"Cache-Control": "public, max-age=86400"})


# -- Route: OG Image -----------------------------------------------------------
@app.get("/og-image.png", include_in_schema=False)
async def get_og_image():
    \"\"\"Serve the Open Graph social preview image (1200x630).\"\"\"\
    p = BASE_DIR / "templates" / "og-image.png"
    if not p.exists():
        raise HTTPException(status_code=404, detail="og-image.png not found")
    return FileResponse(p, media_type="image/png",
                        headers={"Cache-Control": "public, max-age=86400"})

"""

# Insert before the existing PWA Manifest route
insert_marker = "# -- Route: PWA Web App Manifest"
if insert_marker in api:
    api = api.replace(insert_marker, new_routes + insert_marker)
    print("Updated: api/index.py with /favicon.ico, /logo.svg, /og-image.png routes")
else:
    print("WARNING: Could not find PWA route marker in api/index.py")

with open(API_PATH, "w", encoding="utf-8") as f:
    f.write(api)
print("Saved: api/index.py")

print("\nAll logo/favicon/OG assets generated and integrated!")
