"""
Generate PWA assets and mobile-responsive index.html v4 for WealthBridge.
- Creates templates/manifest.json (PWA Web App Manifest)
- Creates templates/sw.js (Service Worker for offline + install)
- Creates PWA icons (192x192, 512x512, 180x180 apple-touch-icon)
- Patches api/index.py to serve manifest.json, sw.js, and PWA icons
"""
from PIL import Image, ImageDraw, ImageFont
import json
import os

BASE = r"c:\Users\sharv\Documents\MarshCase1\MarshCase1"
TEMPLATES = os.path.join(BASE, "templates")


# ─────────────────────────────────────────────────────────────────
# 1. GENERATE PWA ICONS using Pillow
# ─────────────────────────────────────────────────────────────────
def make_icon(size, path):
    # Aqua-blue gradient background with diamond emoji
    img = Image.new("RGB", (size, size), "#FAF8F5")
    draw = ImageDraw.Draw(img)

    # Aqua blue radial-ish gradient via concentric rects
    steps = size // 2
    for i in range(steps, 0, -1):
        ratio = i / steps
        r = int(0 + ratio * 0)
        g = int(131 + ratio * (180 - 131))
        b = int(176 + ratio * (219 - 176))
        color = (r, g, b)
        x0, y0 = steps - i, steps - i
        x1, y1 = steps + i, steps + i
        draw.rectangle([x0, y0, x1, y1], fill=color)

    # Rounded corner mask
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    corner_r = size // 5
    mask_draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=corner_r, fill=255)
    img.putalpha(mask)

    # Draw a "W" letter in white
    text_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    font_size = int(size * 0.52)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = text_draw.textbbox((0, 0), "W", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) // 2 - bbox[0]
    ty = (size - th) // 2 - bbox[1]
    text_draw.text((tx, ty), "W", fill=(255, 255, 255, 255), font=font)

    # Composite
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    result.paste(text_img, (0, 0), text_img)

    result.save(path, "PNG")
    print(f"Generated icon: {path} ({size}x{size})")

make_icon(192, os.path.join(TEMPLATES, "icon-192.png"))
make_icon(512, os.path.join(TEMPLATES, "icon-512.png"))
make_icon(180, os.path.join(TEMPLATES, "apple-touch-icon.png"))


# ─────────────────────────────────────────────────────────────────
# 2. CREATE manifest.json
# ─────────────────────────────────────────────────────────────────
manifest = {
    "name": "WealthBridge",
    "short_name": "WealthBridge",
    "description": "Bridging Today's Income with Tomorrow's Retirement — Premium Retirement Planner",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#FAF8F5",
    "theme_color": "#0083B0",
    "orientation": "portrait-primary",
    "categories": ["finance", "productivity"],
    "icons": [
        {
            "src": "/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ],
    "screenshots": [],
    "shortcuts": [
        {
            "name": "Financial Calculator",
            "url": "/?tab=1",
            "description": "Open Unified Financial Calculator"
        },
        {
            "name": "Wealth Accumulation",
            "url": "/?tab=3",
            "description": "View Wealth Accumulation Layer"
        }
    ]
}

manifest_path = os.path.join(TEMPLATES, "manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
print("Generated manifest.json")


# ─────────────────────────────────────────────────────────────────
# 3. CREATE sw.js (Service Worker)
# ─────────────────────────────────────────────────────────────────
sw_js = """
const CACHE_NAME = 'wealthbridge-v1';
const STATIC_ASSETS = [
  '/',
  '/background-pattern.jpg',
  '/icon-192.png',
  '/icon-512.png',
  '/apple-touch-icon.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js',
  'https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js'
];

// Install: cache all static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS).catch(err => {
        console.warn('[SW] Failed to cache some assets during install:', err);
      });
    })
  );
  self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  return self.clients.claim();
});

// Fetch: stale-while-revalidate for static, network-first for API
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // API calls: always network first, fallback to cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return res;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Static assets: cache first, network fallback
  event.respondWith(
    caches.match(event.request).then(cached => {
      const network = fetch(event.request).then(res => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return res;
      });
      return cached || network;
    })
  );
});
"""

sw_path = os.path.join(TEMPLATES, "sw.js")
with open(sw_path, "w", encoding="utf-8") as f:
    f.write(sw_js.strip())
print("Generated sw.js")

print("\\nAll PWA assets generated. Now update api/index.py and index.html.")
