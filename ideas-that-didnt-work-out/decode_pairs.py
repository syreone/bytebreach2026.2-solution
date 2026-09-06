import itertools

pairs = [("T","R"),("R","Y"),("I","G"),("N","C"),("T","B"),("I","M"),("G","R"),("N","Y"),("A","G"),("N","C"),("T","B")]

with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = set(w.strip().lower() for w in f if w.strip())

found = []
for cand in itertools.product(*pairs):
    s = "".join(cand)
    if s.lower() in words:
        found.append(s)
    r = s[::-1]
    if r.lower() in words:
        found.append(r + " (reverse)")

print("in-order hits:", found)