import urllib.request, urllib.error

for u in ["https://panoplyvalley.onrender.com/v/8f2a1c9d4e7b",
          "https://panoplyvalley.onrender.com/v/8f2a1c9d4e7b/submit",
          "https://panoplyvalley.onrender.com/vault/8f2a1c9d4e7b",
          "https://panoplyvalley.onrender.com/api/v/8f2a1c9d4e7b/submit",
          "https://panoplyvalley.onrender.com/docs",
          "https://panoplyvalley.onrender.com/_archive"]:
    req = urllib.request.Request(u, headers={"User-Agent": "curl/9"})
    try:
        r = urllib.request.urlopen(req, timeout=25)
        print("### GET", url, "->", r.status, r.headers.get("Content-Type"))
        b = r.read()
        print(b[:1500].decode("utf-8", "replace"))
        print("len", len(b))
    except urllib.error.HTTPError as e:
        print("### GET", url, "->", e.code, e.headers.get("Content-Type"))
        try:
            b = e.read()
            print(repr(b[:400]))
        except Exception:
            pass
    print("-"*70)