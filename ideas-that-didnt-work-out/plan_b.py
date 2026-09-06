import itertools

word = "TRINTIGNANT"
keys = ["DD//q4v7", "DDq", "q4v7", "DD", "q4v7nk2xr9tb6mhd", "HOTP", "INHIBIT", "MIRABEL", "PANOPLY"]
letters_only = "".join(c for c in keys[0] if c.isalpha())

def vig(text, key, mode):
    out = ""
    ki = 0
    for ch in text:
        if ch.isalpha():
            k = ord(key[ki % len(key)].upper()) - 65
            base = 65
            x = ord(ch) - 65
            if mode == "e":
                out += chr(65 + (x + k) % 26)
            else:
                out += chr(65 + (x - k) % 26)
            ki += 1
    return out

def caesar(text, shift):
    return "".join(chr(65 + (ord(c) - 65 + shift) % 26) for c in text)

print("=== plan B: keyed transforms of TRINTIGNANT ===")
for k in keys:
    lk = "".join(c for c in k if c.isalpha()) or k
    if not lk:
        continue
    print(k, "->", lk, "| vig(e):", vig(word, lk, "e"), "| vig(d):", vig(word, lk, "d"))

print()
print("=== Caesar all shifts ===")
for s in range(26):
    print(s, caesar(word, -s))

# columnar transposition with keys
def columnar(text, key, decrypt=False):
    n = len(key)
    order = sorted(range(n), key=lambda i: key[i])
    if not decrypt:
        rows = [text[i:i+n] for i in range(0, len(text), n)]
        cols = []
        for oc in range(n):
            i = order[oc]
            cols.append("".join(r[i] for r in rows if i < len(r)))
        return "".join(cols)
    return ""

print()
print("=== columnar transposition ===")
for k in keys:
    lk = "".join(c for c in k if c.isalpha()) or k
    if not lk:
        continue
    print("key", lk, "->", columnar(word, lk))

print()
print("=== key 'DD//q4v7' as a hint: split word by 8 chars? length-based book cipher? ===")
print("len word", len(word), "key pattern lengths as digits 4,2,2,1,2 ...")

# maybe DD//q4v7 encodes shifts per char: D=3 D=3 / / q=16 4 v=21 7 ... use only D,q,v
# or the signature suggests 'pride' ? Actually let me just print per-char deltas needed to make something
print()
print("=== per-char: what delta maps TRINTIGNANT -> candidate Reynolds names? ===")
cands = ["DREYFUS","AURORA","ARORA","PANOPLY","THALIA","CHASM","COIREBEG","ARDMORE","GLITTER","TOMDREYFUS","INHIBIT","MIRABEL","CHALMERS","SPARVER","SHACKLETON"]
for c in cands:
    if len(c) == len(word):
        d = [ord(a)-ord(b) for a,b in zip(c, word)]
        print(c, d, set(d))

# try: maybe word must be shifted to real Reynolds name
print()
print("=== does TRINTIGNANT appear in a Reynolds novel? placeholder: search later ===")