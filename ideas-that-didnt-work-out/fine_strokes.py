import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
sr = w.getframerate(); a = array.array("h", w.readframes(w.getnframes()))
ch = w.getnchannels()
mono = [a[i] for i in range(0, len(a), ch)]

def fine(t0, t1, cols=140, rows=18, gain=None, label=""):
    s0 = int(t0*sr); s1 = int(t1*sr)
    seg = mono[s0:s1]
    step = max(1, len(seg)//cols)
    win = max(1, step//8)
    amp = max(abs(min(seg)), abs(max(seg))) if gain is None else gain
    grid = [[" "] * cols for _ in range(rows)]
    for c in range(cols):
        chunk = seg[c*step:(c+1)*step]
        mx = max(abs(x) for x in chunk) if chunk else 0
        r = min(rows-1, int(mx/amp*(rows-1)))
        for k in range(r+1):
            grid[rows-1-k][c] = "#"
    print("###", label, amp/32768)
    for row in grid:
        print("".join(row))
    print()

for (t0,t1,name) in [(1.00,2.60,"s1"),(3.10,4.17,"s2"),(4.75,6.25,"s3"),
                     (6.77,8.23,"s4"),(8.54,10.08,"s5"),(10.50,12.02,"s6"),(12.46,13.96,"s7")]:
    # loudest stroke s1 sets the manual gain for all
    fine(t0, t1, 140, 18, gain=7900, label=name)