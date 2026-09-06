import re

with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = [w.strip() for w in f]

def ok(w):
    if len(w) != 11:
        return False
    return (w[0] == w[6] and w[1] == w[7] and w[2] == w[8]
            and w[3] == w[9] and w[4] == w[10])

hits = [w.upper() for w in words if ok(w)]
print("words with color-pattern (X0=X6, X1=X7, X2=X8, X3=X9, X4=X10):")
for h in hits:
    print(" ", h)
print(len(hits), "hits")