import numpy as np
from scipy.io import wavfile
from scipy import signal
from PIL import Image

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)

f, t, Sxx = signal.spectrogram(x, rate, nperseg=1024, noverlap=768)
S = 10*np.log10(Sxx + 1e-12)

# restrict to band 100..8000
band = (f >= 100) & (f <= 8000)
fb = f[band]
Sb = S[band, :]

f0 = np.zeros(Sb.shape[1])
for i in range(Sb.shape[1]):
    j = np.argmax(Sb[:, i])
    f0[i] = fb[j]

print("f0 min/max:", f0.min(), f0.max(), "windows:", len(f0))
# plot trace as black on white
W = len(f0)
H = 180
tr = np.full((H, W), 1.0)
yf = np.clip((f0 - 100.0)/(8000.0-100.0), 0, 1)
for i, v in enumerate(yf):
    r = int(round((1 - v) * (H-1)))
    for d in range(-1, 2):
        rr = r + d
        if 0 <= rr < H:
            tr[rr, i] = 0.0

# render ASCII at reasonable width
width = 300
im = Image.fromarray((tr*255).astype(np.uint8))
leg = im.resize((width, int(H*width/W*0.5)), Image.LANCZOS)
g = np.array(leg).astype(float)
g = (g - g.min())/(g.max()-g.min()+1e-9)
cm = " .:-=+*#%@"
lines = ["".join(cm[min(int((1-g[r,c])*10),9)] for c in range(width)) for r in range(g.shape[0])]
open("f0trace.txt","w").write("\n".join(lines))
print("saved f0trace.txt")
# save image too
im = Image.fromarray((tr*255).astype(np.uint8)).resize((3000, 900), Image.LANCZOS)
im.save("f0trace.png")