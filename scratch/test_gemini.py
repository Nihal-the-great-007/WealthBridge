import json
import urllib.request
import urllib.error
import os

key = os.environ.get("GEMINI_API_KEY", "")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"

headers = {"Content-Type": "application/json"}
data = {
    "contents": [{"parts": [{"text": "Hello, this is a test. Reply with 'Ok' if you receive this."}]}]
}

req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        res_body = response.read().decode("utf-8")
        res_json = json.loads(res_body)
        print("Success! Response:")
        print(json.dumps(res_json, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
