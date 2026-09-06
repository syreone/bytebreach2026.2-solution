import urllib.request, urllib.error

base = "https://panoplyvalley.onrender.com/_archive/"
names = ["claims", "claims.txt", "vault", "vault.txt", "vault.json", "works", "works.txt",
         "ledgers", "ledgers.txt", "ledger", "ledger.txt", "records", "records.txt",
         "sittings", "sittings.txt", "sitting", "sitting.txt", "assets", "assets.txt",
         "list", "index", "index.txt", "inventory", "inventory.txt", "manifest",
         "manifest.txt", "contents", "contents.txt", "portfolio", "portfolio.txt",
         "galleries", "gallery.txt", "gallery", "paintings.txt", "paintings",
         "authors", "authors.txt", "artists.txt", "artist.txt", "people.txt",
         "index.json", "data.json", "claim.json", "claims.json", "vault.txt.gz",
         "claims.txt.gz", "boxes", "box", "books", "books.txt", "yard", "yard.txt",
         "office", "office.txt", "log", "log.txt", "archive", "archive.txt",
         "sideboard", "sideboard.txt", "station", "station.txt", "fares", "fares.txt",
         "timetables", "timetable.txt", "up", "down", "ledgers/", "works/",
         "inhibit", "mirabel", "coding", "code", "hint", "hints.txt", "answers.txt"]

def hit(name):
    url = base + name
    req = urllib.request.Request(url, headers={"x-station": "q4v7nk2xr9tb6mhd"})
    try:
        r = urllib.request.urlopen(req, timeout=15)
        return r.status, r.read()[:200]
    except urllib.error.HTTPError as e:
        return e.code, None

for n in names:
    s, body = hit(n)
    tag = ""
    if body:
        tag = " | " + body[:180].decode("utf-8", "replace").replace("\n", " ")
    if s != 404:
        print(n, "->", s, tag)
print("sweep done")