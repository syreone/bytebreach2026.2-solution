import numpy as np
from scipy.io import wavfile
rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)

x = L[16*rate:30*rate]
y = R[16*rate:30*rate]
wx = 649; hy = 220
xr = (x.min(), x.max()); yr = (y.min(), y.max())
cols = np.clip(((x - xr[0])/(xr[1]-xr[0])*(wx-1)).astype(int), 0, wx-1)
rows = np.clip(((y - yr[0])/(yr[1]-yr[0])*(hy-1)).astype(int), 0, hy-1)
img = np.zeros((hy, wx), dtype=int)
for c, r in zip(cols, rows):
    img[r, c] += 1
v = img
cm = " .:-=+*#%@"
lines = []
for r in range(hy-1, -1, -1):
    lines.append("".join(cm[min(v[r,c], len(cm)-1)] for c in range(wx)))
open("segB_649.txt","w").write("\n".join(lines))
print("done", wx, hy)