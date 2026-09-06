import urllib.request, urllib.error, time

for p in ["inhibit", "mirabel", "up", "down", "station", "ledgers.txt", "works.txt",
          "fares", "timetables", "ledgers", "works"]:
    url = "https://panoplyvalley.onrender.com/" + p
    req = urllib.request.Request(url, headers={"x-station": "q4v7nk2xr9tb6mhd", "User-Agent": "curl/9"})
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        print("###", p, "->", resp.status, resp.headers.get("Location"), "len", len(resp.read()))
    except urllib.error.HTTPError as e:
        print("###", p, "->", e.code, e.headers.get("Location"))
    time.sleep(2.0)