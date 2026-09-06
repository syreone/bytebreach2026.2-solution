import urllib.request, urllib.error, time

def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=25)
        return r.status, r.headers.get("Location"), r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location"), e.headers.get("Content-Type"), e.read() if hasattr(e, "read") else None

names = ["station", "stations", "up", "down", "inhibit", "mirabel",
         "works", "ledgers.txt", "ledgers", "fares", "timetables",
         "archive", "log", "valuation"]
for h in [{"User-Agent": "curl/9"}, {"x-station": "q4v7nk2xr9tb6mhd", "User-Agent": "curl/9"}]:
    for nm in names:
        url = "https://panoplyvalley.onrender.com/" + nm
        st, loc, ct, body = get(url, h)
        head = ""
        if st == 200:
            head = (body[:600].decode("utf-8", "replace") if body else "")
        tag = "HDR" if "x-station" in h else "   "
        print("[%s] /%-14s -> %d loc=%s ct=%s" % (tag, nm, st, loc, ct))
        if st == 200 and head:
            print("     ", head.replace("\n", " | ")[:500])
    time.sleep(0.4)