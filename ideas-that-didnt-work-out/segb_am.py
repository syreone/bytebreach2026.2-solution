import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
sr = w.getframerate(); a = array.array("h", w.readframes(w.getnframes()))
ch = w.getnchannels()
mono = [a[i] for i in range(0, len(a), ch)]
sB = int(15.0*sr); sE = int(30.0*sr)
seg = mono[sB:sE]

# per-block RMS at ~10ms resolution
win = sr//100
rms = []
for i in range(0, len(seg)-win, win):
    c = seg[i:i+win]
    rms.append((sum(x*x for x in c)/len(c))**.5)

mx = max(rms)
# is there more than one distinct amplitude level?
levels = sorted(set(round(r/mx, 2) for r in rms))
print("distinct normalized levels:", levels[:50], "count", len(levels))

# hist of normalized values
hist = {}
for r in rms:
    k = round(10*r/mx)
    hist[k] = hist.get(k,0)+1
print("hist (x/10 of max):", sorted(hist.items()))