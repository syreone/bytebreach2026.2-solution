import itertools

v = [84, 82, 73, 78, 84, 73, 71, 78, 65, 78, 84]  # length//3 ASCII codes
c = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4]              # color index

with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = set(w.strip().upper() for w in f)
words11 = {w for w in words if len(w) == 11}

def letters(a, b, d, order, nc=26):
    return "".join(
        chr(65 + ((a * (v[i] - 65) + b * c[i] + d) % nc)) for i in order)

hits = []
for a in range(1, 26):
    for b in range(26):
        for d in range(26):
            for order in (range(11), range(10, -1, -1)):
                w = letters(a, b, d, order)
                if w in words11:
                    hits.append((a, b, d, "fwd" if order == range(11) else "rev", w))

print("affine (v,c) hits:", hits)

# also one formula on color VALUE A1Z26 (R=18,Y=25,...)
ck = [18, 25, 7, 3, 2, 13, 18, 25, 7, 3, 2]
hits2 = []
for a in range(1, 26):
    for b in range(26):
        for d in range(26):
            for order in (range(11), range(10, -1, -1)):
                w = "".join(chr(65 + ((a * (v[i] - 65) + b * ck[i] + d) % 26)) for i in order)
                if w in words11:
                    hits2.append((a, b, d, "fwd" if order == range(11) else "rev", w))
print("affine (v,colorletter) hits:", hits2)