import urllib.request, urllib.error, time

paths = ["_archive/dd/q4v7/", "_archive/dd.txt/", "_archive/q4v7/",
         "_archive/q4v7.txt/", "_archive/dd/", "_archive/log.txt"]
for p in paths:
    url = "https://panoplyvalley.onrender.com/" + p
    req = urllib.request.Request(url, headers={"x-station": "q4v7nk2xr9tb6mhd", "User-Agent": "curl/9"})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        print("###", p, "->", r.status, "len", len(r.read()))
    except urllib.error.HTTPError as e:
        print("###", p, "->", e.code)
    time.sleep(2.0)