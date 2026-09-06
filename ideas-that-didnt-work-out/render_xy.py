import numpy as np
from scipy.io import wavfile

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)
n = len(L)

def scatter_render(x, y, wx=240, hy=None, xr=None, yr=None, thr=0, label=""):
    if xr is None:
        xr = (x.min(), x.max())
    if yr is None:
        yr = (y.min(), y.max())
    if hy is None:
        hy = int(round(wx/2))
    cols = np.clip(((x - xr[0])/(xr[1]-xr[0])*(wx-1)).astype(int), 0, wx-1)
    rows = np.clip(((y - yr[0])/(yr[1]-yr[0])*(hy-1)).astype(int), 0, hy-1)
    img = np.zeros((hy, wx), dtype=int)
    for c, r in zip(cols, rows):
        img[r, c] += 1
    v = img.copy()
    cm = " .:-=+*#%@"
    if thr:
        v = (v >= thr).astype(int)
    lines = []
    for r in range(hy-1, -1, -1):
        line = "".join(cm[min(v[r,c], len(cm)-1)] for c in range(wx))
        lines.append(line)
    out = "\n".join(lines)
    open("%s.txt" % label, "w").write(out)
    print(label, "xrange", xr, "yrange", yr, "points", len(x))
    return out

# segA strokes t=1..13s
ia = (L[1*rate:13*rate], R[1*rate:13*rate])
# segB continuous pass t=16..30
ib = (L[16*rate:30*rate], R[16*rate:30*rate])

# segB (L,R): letters should appear. Use full ranges.
scatter_render(*ib, xr=(-32000,32000), yr=(-21000,21000), wx=300, hy=150, label="segB_full")
# zoom into signed content? try symmetric
scatter_render(*ib, xr=(-32000,32000), yr=(-21000,21000), wx=600, hy=300, label="segB_big")
# segA as (L, dL) phase: derivative
dL = np.diff(L)
scatter_render(L[1*rate:13*rate-1], dL[1*rate:13*rate-1], xr=None, yr=None, wx=300, hy=150, label="segA_dL")