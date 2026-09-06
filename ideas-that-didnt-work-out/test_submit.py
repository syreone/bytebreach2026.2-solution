import urllib.request, urllib.error, json, time

cands = ["TRINTIGNANT", "DISNEYLAND", "TOGETHER", "MIRABEL", "INHIBIT", "MELODIA", "TRAIN"]
seen = set()
for c in cands:
    if c.upper() in seen: continue
    seen.add(c.upper())
    body = json.dumps({"password": "inhibit mirabel " + c}).encode()
    req = urllib.request.Request("https://panoplyvalley.onrender.com/v/8f2a1c9d4e7b/submit",
                                 data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=20)
        print("### %-12s -> 200 %r" % (c, r.read().decode()))
    except urllib.error.HTTPError as e:
        print("### %-12s -> %d %r" % (c, e.code, e.read().decode()))
    time.sleep(1.5)