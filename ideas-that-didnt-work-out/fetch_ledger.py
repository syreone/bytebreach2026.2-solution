import urllib.request, urllib.error, time

paths = ["_archive/ledgers.txt/", "_archive/ledgers/", "_archive/index.html",
         "_archive/Ledgers", "_archive/ledger", "_archive/ledgers.html",
         "_archive/ledgers.txt", "_archive/ledgers/index.html"]
for p in paths:
    url = "https://panoplyvalley.onrender.com/" + p
    req = urllib.request.Request(url, headers={"x-station": "q4v7nk2xr9tb6mhd", "User-Agent": "curl/8"})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        body = r.read()
        print("###", p, "->", r.status, "len", len(body))
        print(body[:2500].decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        print("###", p, "->", e.code)
    time.sleep(1.5)