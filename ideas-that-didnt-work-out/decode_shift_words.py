import sys

lenchars = "TRINTIGNANT"
colchars = "RYGCBMRYGCB"

with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = [w.strip().upper() for w in f]

n = len(lenchars)
colors = set(colchars)

def shifts_for(word):
    for mode in ("cipher-k", "cipher+k"):
        shift = {}
        ok = True
        for c, w in zip(colchars, word):
            ci = ord(c) - 65
            wi = ord(w) - 65
            if mode == "cipher-k":
                s = (ci - wi) % 26  # plaintext = cipher - shift
            else:
                s = (wi - ci) % 26
            if c in shift and shift[c] != s:
                ok = False
                break
            shift[c] = s
        if ok and len(shift) == len(colors):
            print(f"{mode:8s} word={word} shifts=" +
                  "".join(f"{cc}:{shift[cc]}" for cc in colors))

count = 0
for w in words:
    if len(w) != n:
        continue
    count += 1
    shifts_for(w)
print("checked", count)