from collections import Counter

s = "TRINTIGNANT"
m = Counter(s)
with open(r"C:\Users\Luka\AppData\Local\Temp\opencode\words_alpha.txt") as f:
    words = [w.strip().upper() for w in f]

hits = []
for w in words:
    if len(w) == 11 and Counter(w) == m:
        hits.append(w)
print("exact 11-letter anagrams:", hits)

# also check whether s is an anagram of ANY word (n letters) exactly
exact = [w for w in words if Counter(w) == m]
print(len(exact), "exact anagrams total")