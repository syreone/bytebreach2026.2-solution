import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
raw = w.readframes(n)
a = array.array("h", raw)
mono = [a[i] for i in range(0, len(a), ch)]

def render(s0, s1, cols, rows, label, amp=None):
    seg = mono[s0:s1]
    if amp is None:
        amp = max(abs(min(seg)), abs(max(seg))) or 1
    step = max(1, len(seg) // cols)
    nrow = min(len(seg)//step, cols)
    # bucket per column: max abs | use max and min
    grid = [[" "] * cols for _ in range(rows)]
    for c in range(nrow):
        chunk = seg[c*step:(c+1)*step]
        mx = max(abs(min(chunk)), abs(max(chunk)))
        r = min(rows-1, int(mx / amp * (rows-1)))
        r = max(r, 0)
        for k in range(r+1):
            if rows-1-k >= 0:
                grid[rows-1-k][c] = "#"
    print(label, "amp=%.4f" % (amp/32768))
    for row in grid[::2]:
        print("".join(row))
    print()

# whole file fixed at segA scale to see shape; and segA alone
total = len(mono)
# peak of first 13.5s for manual gain
segA = mono[0:int(15.0*sr)]
ampA = max(abs(min(segA)), abs(max(segA)))
render(0, total, 220, 44, "FULL (gain set from segA peak)", amp=ampA)
render(0, int(15.0*sr), 220, 44, "SEG A envelope", amp=ampA)