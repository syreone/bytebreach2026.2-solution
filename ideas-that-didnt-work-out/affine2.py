import itertools

v = [84, 82, 73, 78, 84, 73, 71, 78, 65, 78, 84]     # h//3
rank = [5, 4, 2, 3, 5, 2, 1, 3, 0, 3, 5]             # length rank 195->0
cidx = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4]             # color index
ck = [18, 25, 7, 3, 2, 13, 18, 25, 7, 3, 2]          # color letter A1Z26

with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = set(w.strip().upper() for w in f)

def search(X, Y, label):
    hits = []
    n = len(X)
    for A in range(0, 26):
        for B in range(-26, 27):
            for C in range(0, 96):
                vals = [A * X[i] + B * Y[i] + C for i in range(n)]
                if all(65 <= x <= 90 for x in vals) or all(97 <= x <= 122 for x in vals):
                    w = "".join(chr(x) for x in vals).upper()
                    r = w[::-1]
                    if w in words:
                        hits.append((A, B, C, "fwd", w))
                    if r in words:
                        hits.append((A, B, C, "rev", r))
    print(label, "hits:", hits[:20])

search(v, cidx, "(h//3, coloridx)")
search(v, ck, "(h//3, colorletter)")
search(rank, cidx, "(rank, coloridx)")
search(rank, ck, "(rank, colorletter)")
search(cidx, v, "(coloridx, h//3)")
search(ck, v, "(colorletter, h//3)")