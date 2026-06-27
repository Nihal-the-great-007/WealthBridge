import requests, os
os.environ['PYTHONIOENCODING'] = 'utf-8'

BASE = "http://127.0.0.1:8000"

def check(url, expected_ct=None):
    try:
        r = requests.get(url, timeout=5)
        ct = r.headers.get("content-type", "")
        ok = r.status_code == 200
        type_ok = expected_ct is None or expected_ct in ct
        status = "OK  " if (ok and type_ok) else "FAIL"
        print(f"[{status}] {url} -> {r.status_code} | {len(r.content):,} bytes | {ct[:55]}")
        return ok
    except Exception as e:
        print(f"[ERR ] {url} -> {e}")
        return False

print("=== WealthBridge Full Asset Verification ===\n")
print("-- Core --")
check(f"{BASE}/",              "text/html")
check(f"{BASE}/api/data",      "application/json")

print("\n-- Favicon & Logo --")
check(f"{BASE}/favicon.ico",        "image/x-icon")
check(f"{BASE}/logo.svg",           "image/svg+xml")
check(f"{BASE}/og-image.png",       "image/png")

print("\n-- PWA Assets --")
check(f"{BASE}/manifest.json",       "manifest")
check(f"{BASE}/sw.js",               "javascript")
check(f"{BASE}/icon-192.png",        "image/png")
check(f"{BASE}/icon-512.png",        "image/png")
check(f"{BASE}/apple-touch-icon.png","image/png")
check(f"{BASE}/background-pattern.jpg","image")

print("\n=== Done ===")
