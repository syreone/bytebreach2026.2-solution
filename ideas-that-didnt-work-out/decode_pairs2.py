import itertools

bars = [
    (84, 0), (82, 1), (73, 2), (78, 3), (84, 4), (73, 5),
    (71, 0), (78, 1), (65, 2), (78, 3), (84, 4),
]

with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = set(w.strip().lower() for w in f if w.strip())

def opt1(v, c):  # plain letter only
    return [chr(v)]

def opt3(v, c):  # plain, +color, -color
    return [chr(v), chr(((v - 65 + c) % 26) + 65), chr(((v - 65 - c) % 26) + 65)]

def opt5(v, c):  # plus color letters from name A1Z26
    return [chr(v), chr(((v - 65 + c) % 26) + 65), chr(((v - 65 - c) % 26) + 65),
            chr(((v - 65 + max(0, c - 3)) % 26) + 65), chr(((v - 65 - max(0, c - 3)) % 26) + 65)]

for name, gen in [("opt3", opt3), ("opt5", opt5)]:
    hits = set()
    for cand in itertools.product(*[gen(v, c) for v, c in bars]):
        s = "".join(cand).upper()
        if s.lower() in words:
            hits.add(s)
        r = s[::-1]
        if r.lower() in words:
            hits.add(r + "(rev)")
    print(name, "hits:", list(hits))

# interleavings of length & color strings
lenchars = "".join(chr(v) for v, _ in bars)    # T R I N T I G N A N T
colchars = "RYGCBMRYGCB"
print("lenchars:", lenchars)
combos = {
    "len+col interleave": "".join(a + b for a, b in zip(lenchars, colchars)),
    "col+len interleave": "".join(a + b for a, b in zip(colchars, lenchars)),
    "len+col concat": lenchars + colchars,
    "col+len concat": colchars + lenchars,
    "len even,col odd": lenchars[0::2] + colchars[1::2],
}
for k, v in combos.items():
    w = v.lower()
    print(k, v, "->", v[::-1], "| word?", w in words or w[::-1] in words)

# reorder length letters by color group
bycolor = {"R": [], "Y": [], "G": [], "C": [], "B": [], "M": []}
order = {"R": 0, "Y": 1, "G": 2, "C": 3, "B": 4, "M": 5}
for (v, _), cc in zip(bars, colchars):
    bycolor[cc].append(chr(v))
for key in ["RGBYCM", "RYGCBM", "B C G M R Y".replace(" ", "")]:
    s = "".join(bycolor[k] for k in key if k in bycolor)
    print("color-order", key, s, "word?", s.lower() in words)