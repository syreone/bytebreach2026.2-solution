import urllib.request, urllib.error, time

names = ["index", "index.html", "stations", "station", "log", "claims",
         "inhibit", "inhibit.txt", "mirabel", "mirabel.txt",
         "ledgers", "ledgers.txt", "works", "works.txt", "readme", "all"]
for nm in names:
    for ext in ("", ".txt", ".html"):
        u = "https://panoplyvalley.onrender.com/_archive/" + nm + ext
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "curl/9"}), timeout=20)
            b = r.read()
            print("###", u, "->", r.status, "len", len(b))
            print(b[:600].decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code != 404:
                print("###", u, "->", e.code, repr(e.read()[:200]))
        time.sleep(0.35)