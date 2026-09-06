import numpy as np
from scipy.io import wavfile
from scipy import signal
from PIL import Image

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)

f, t, Sxx = signal.spectrogram(x, rate, nperseg=256, noverlap=128)
S = 10*np.log10(Sxx + 1e-12)

# log frequency axis 80..8000
fmin, fmax = 80.0, 8000.0
band = (f >= fmin) & (f <= fmax)
fb = f[band]
Sb = S[band, :]
# redraw onto log-freq raster of height H
H = 900
loglo, loghi = np.log10(fmin), np.log10(fmax)
idx = (np.log10(fb) - loglo)/(loghi - loglo)
img = np.zeros((H, Sb.shape[1]))
for i in range(len(fb)):
    r = int(round((1 - idx[i]) * (H-1)))
    img[r, :] = np.maximum(img[r, :], Sb[i, :])

# contrast stretch
img = img - img.min()
img = img / (np.percentile(img, 99.9) + 1e-9)
img = np.clip(img, 0, 1)
# bright trace: use sqrt to open up
disp = np.sqrt(img)
pil = Image.fromarray((disp*255).astype(np.uint8), 'L')
pil = pil.resize((pil.size[0]*1, int(H* pil.size[0]/pil.size[1] * 0.35)), Image.LANCZOS)
pil.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\spec_full.png')
print("ts:", t[0], t[-1], "bins", len(t))
# also render segA and segB
for name, t0, t1 in [('A', 1.0, 15.0), ('B', 16.0, 30.0)]:
    m = (t >= t0) & (t <= t1)
    sub = img[:, m]
    sp = Image.fromarray((sub*255).astype(np.uint8), 'L')
    sp = sp.resize((int(sp.size[0]*2), int(sp.size[1]*1.2)), Image.LANCZOS)
    sp.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\spec_%s.png' % name)
print("saved")