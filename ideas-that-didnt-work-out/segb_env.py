import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
sr = w.getframerate(); a = array.array("h", w.readframes(w.getnframes()))
ch = w.getnchannels()
mono = [a[i] for i in range(0, len(a), ch)]

def env_render(s0, s1, cols, rows, amp=None, win=None, label=""):
    seg = mono[s0:s1]
    peak = max(abs(min(seg)), abs(max(seg))) if amp is None else amp
    step = max(1, len(seg)//cols)
    win = win or max(1, step//4)
    grid = [[" "] * cols for _ in range(rows)]
    for c in range(cols):
        chunk = seg[c*step:(c+1)*step]
        mx = max(abs(min(chunk)), abs(max(chunk))) if chunk else 0
        r = min(rows-1, int(mx/peak*(rows-1)))
        for k in range(r+1):
            grid[rows-1-k][c] = "#"
    print(label, "win", win, "amp", round(peak/32768,4), "samples", len(seg))
    for row in grid:
        print("".join(row))
    print()

# segB envelope with small window: 40s? segB = 15-30s
sB = int(15.0*sr); sE = int(30.0*sr)
seg = mono[sB:sE]
peakB = max(abs(min(seg)), abs(max(seg)))
env_render(sB, sE, 220, 30, amp=peakB, win=sr//200, label="SEG B (gated?)")
env_render(sB, sE, 220, 30, amp=peakB/4, win=sr//500, label="SEG B zoom gain x4")