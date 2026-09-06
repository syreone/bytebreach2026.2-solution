hs = [252,246,219,234,252,219,213,234,195,234,252]
cols = ['R','Y','G','C','B','M']
# heights -> letters by h//3 (ASCII) and A1Z26
hl = [chr(h//3) for h in hs]
print("h//3 letters:", "".join(hl))
ci = [cols.index(c) for c in ['R','Y','G','C','B','M','R','Y','G','C','B']]  # n/a, we'll list explicitly
colseq = ['R','Y','G','C','B','M','R','Y','G','C','B']
print("colors:", "".join(colseq))

def rot(s, n):
    out = []
    for ch in s:
        if 'A' <= ch <= 'Z':
            out.append(chr((ord(ch)-65+n)%26+65))
        else:
            out.append(ch)
    return "".join(out)

def atbash(s):
    return "".join(chr(90-(ord(c)-65)) if 'A'<=c<='Z' else c for c in s)

base = "".join(hl)
cands = {}
cands['plain'] = base
cands['rev'] = base[::-1]
for n in range(26):
    cands['rot%d'%n] = rot(base, n)
cands['atbash'] = atbash(base)

# combine with color: shift each letter by color index
cand = ""
for i, ch in enumerate(base):
    cand += rot(ch, ci_ if False else colseq[i] and 0 or 0, 0) if False else rot(ch, 0 if colseq[i] in 'RYGCBM' else 0)
# proper: shift by color index
def shift_each(s, shifts):
    out = ""
    for i, ch in enumerate(s):
        out += rot(ch, shifts[i % len(shifts)])
    return out

cidx = ['R','Y','G','C','B','M'].index if False else None
cvals = ['R','Y','G','C','B','M','R','Y','G','C','B']
shifts = [{'R':0,'Y':1,'G':2,'C':3,'B':4,'M':5}[c] for c in cvals]
cands['len+color-shift'] = shift_each(base, shifts)
cands['color+len-shift'] = shift_each(base, [-s for s in shifts])

# per-bar value = h//3 as ascii minus color-shift
val = []
for i,h in enumerate(hs):
    n = h//3 - shifts[i]
    val.append(chr(n))
cands['len-ascii-minus-coloridx'] = "".join(val)
val = [chr(h//3 + shifts[i]) for i,h in enumerate(hs)]
cands['len-ascii-plus-coloridx'] = "".join(val)

# base36 / A1Z26 combining
hvals = sorted(set(hs))
cvals2 = ['R','Y','G','C','B','M']
hidx = {v:i for i,v in enumerate(hvals)}
cidx2 = {c:i for i,c in enumerate(cvals2)}
seq = []
for i,h in enumerate(hs):
    hi, ciN = hidx[h], cidx2[cvals[i]]
    seq.append(hi*6+ciN)
print("h*6+c:", seq, "".join(chr(65+v-1) if v<26 else '?' for v in seq))  # A1Z26 0-based
seq2 = [cidx2[cvals[i]]*6+hidx[hs[i]] for i in range(len(hs))]
print("c*6+h:", seq2, "".join(chr(65+v-1) if v<26 else '?' for v in seq2))

for k,v in cands.items():
    print(k, "->", v)