import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
sr = w.getframerate(); a = array.array("h", w.readframes(w.getnframes()))
ch = w.getnchannels()
L = [a[i] for i in range(0, len(a), ch)]
R = [a[i] for i in range(1, len(a), ch)]

def render(seg, cols, rows, gain=None, label=""):
    peak = max(abs(min(seg)), abs(max(seg))) if gain is None else gain
    step = max(1, len(seg)//cols)
    win = max(1, step)
    grid = [[" "] * cols for _ in range(rows)]
    for c in range(cols):
        chunk = seg[c*step:(c+1)*step]
        mx = max(abs(x) for x in chunk) if chunk else 0
        r = min(rows-1, int(mx/peak*(rows-1))) if peak else 0
        for k in range(r+1):
            grid[rows-1-k][c] = "#"
    print(label, "peak", round(peak/32768,4))
    for row in grid:
        print("".join(row))
    print()

total = len(R)
pR = max(abs(min(R)), abs(max(R)))
# right channel over full 30s, envelope, high resolution
render(R, 250, 24, gain=pR, label="R full, auto-gain")
render(R, 250, 24, gain=16000, label="R full, gain=16000")
render(R[0:int(15*sr)], 250, 24, gain=16000, label="R 0-15s gain 16000")