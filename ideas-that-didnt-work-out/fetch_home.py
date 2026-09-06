import urllib.request, urllib.error

def fetch(url, headers=None, timeout=25):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "curl/9"})
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if hasattr(e, "read") else None

base = "https://panoplyvalley.onrender.com"
st, body = fetch(base)
open(r"C:\Users\Luka\cerberus-99-git\home.html", "wb").write(body)
print("status", st, "len", len(body))
print(body.decode("utf-8", "replace"))