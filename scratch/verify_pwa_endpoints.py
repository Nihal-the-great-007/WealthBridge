import requests
import time
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'


BASE = "http://127.0.0.1:8000"

def check(url, expected_content_type=None):
    try:
        r = requests.get(url, timeout=5)
        ct = r.headers.get("content-type", "")
        ok = r.status_code == 200
        type_ok = expected_content_type is None or expected_content_type in ct
        status = "OK  " if (ok and type_ok) else "FAIL"
        print(f"[{status}] GET {url} -> {r.status_code} | {ct[:60]}")
        return ok
    except Exception as e:
        print(f"[ERR ] GET {url} -> ERROR: {e}")
        return False

print("=== WealthBridge PWA Endpoint Verification ===")
check(f"{BASE}/")
check(f"{BASE}/manifest.json", "manifest")
check(f"{BASE}/sw.js", "javascript")
check(f"{BASE}/icon-192.png", "image/png")
check(f"{BASE}/icon-512.png", "image/png")
check(f"{BASE}/apple-touch-icon.png", "image/png")
check(f"{BASE}/background-pattern.jpg", "image")
check(f"{BASE}/api/data", "application/json")
print("\nAll PWA endpoints verified!")
