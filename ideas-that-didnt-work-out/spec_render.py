import numpy as np
from scipy.io import wavfile
from scipy import signal
from PIL import Image

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)
f, t, Sxx = signal.spectrogram(x, rate, nperseg=512, noverlap=448)
S = 10*np.log10(Sxx + 1e-12)

def render(t0, t1, fmin, fmax, log, height, width, path, thr=None):
    m = (t >= t0) & (t <= t1)
    band = (f >= fmin) & (f <= fmax)
    fb = f[band]
    Sb = S[band, :][:, m]
    if log:
        lo, hi = np.log10(fmin), np.log10(fmax)
        idx = np.log10(fb)
    else:
        lo, hi = fmin, fmax
        idx = fb
    H, Wt = height, Sb.shape[1]
    img = np.zeros((H, Wt))
    for i in range(len(fb)):
        r = int(round((1 - (idx[i]-lo)/(hi-lo)) * (H-1)))
        img[r, :] = np.maximum(img[r, :], Sb[i, :])
    img = img - np.percentile(img, 40)
    img = img / (np.percentile(img, 99) - np.percentile(img, 40) + 1e-9)
    img = np.clip(img, 0, 1)
    if thr is not None:
        b = (img > thr).astype(np.uint8)*255
    else:
        b = (np.sqrt(img)*255).astype(np.uint8)
    scale = width / Wt
    out = Image.fromarray(b, 'L').resize((width, int(H*scale)), Image.LANCZOS) if scale != 1 else Image.fromarray(b, 'L')
    out.save(path)
    print(path, out.size)

render(16.0, 30.0, 40, 2000, True, 700, 2200, r'C:\Users\Luka\AppData\Local\Temp\opencode\sb_low_log.png', thr=0.35)
render(16.0, 30.0, 40, 800, True, 700, 2200, r'C:\Users\Luka\AppData\Local\Temp\opencode\sb_low_log2.png', thr=0.30)
render(16.0, 30.0, 40, 2000, False, 700, 2200, r'C:\Users\Luka\AppData\Local\Temp\opencode\sb_low_lin.png', thr=0.30)
render(1.0, 15.0, 40, 2000, True, 700, 2200, r'C:\Users\Luka\AppData\Local\Temp\opencode\sa_low_log.png', thr=0.30)
render(16.0, 30.0, 0, 1000, False, 900, 2400, r'C:\Users\Luka\AppData\Local\Temp\opencode\sb_01700_lin.png', thr=None)
render(16.0, 30.0, 40, 1000, True, 900, 2400, r'C:\Users\Luka\AppData\Local\Temp\opencode\sb_01000_log.png', thr=None)