import urllib.request, urllib.error

def fetch(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "curl/9"})
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.status, r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), None

base = "https://panoplyvalley.onrender.com"
for path, hd in [("", {}),
                 ("/robots.txt", {}),
                 ("/sitemap.xml", {}),
                 ("/v/8f2a1c9d4e7b", {}),
                 ("/v/8f2a1c9d4e7b", {"x-station": "q4v7nk2xr9tb6mhd"}),
                 ("/", {"x-station": "q4v7nk2xr9tb6mhd"}),
                 ("/ledgers", {"x-station": "q4v7nk2xr9tb6mhd"}),
                ]:
    st, ct, body = fetch(base + path, hd)
    if body is not None and len(body) > 4000:
        body = body[:4000]
    print("###", path or "/", "hdr", bool(hd), "->", st, ct)
    if body:
        print(body.decode("utf-8", "replace")[:1800])
    print("-"*80)