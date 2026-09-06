import numpy as np
from scipy.io import wavfile
from scipy import signal
from PIL import Image

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)
from scipy.signal import spectrogram as _sp
f, t, Sxx = _sp(x, rate, nperseg=512, noverlap=448)
S = 10*np.log10(Sxx + 1e-12)

def render(t0, t1, fmin, fmax, log, height, width, path, thr=None, anti=0):
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
    H = height
    Wt = Sb.shape[1]
    img = np.zeros((H, Wt))
    for i in range(len(fb)):
        r = int(round((1 - (idx[i]-lo)/(hi-lo)) * (H-1)))
        img[r, :] = np.maximum(img[r, :], Sb[i, :])
    img = img - np.percentile(img, anti)
    img = img / (np.percentile(img, 99.5) - np.percentile(img, anti) + 1e-9)
    img = np.clip(img, 0, 1)
    if thr is not None:
        b = (img > thr).astype(np.uint8)*255
    else:
        b = (np.sqrt(img)*255).astype(np.uint8)
    # anti-alias to final width keeping height
    if Wt != width:
        full = Image.fromarray(b, 'L')
        out = full.resize((width, H), Image.LANCZOS)
    else:
        out = Image.fromarray(b, 'L')
    out.save(path)
    print(path, out.size)

# seg B low
render(16.0, 30.0, 40, 1200, True, 800, 2000, r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_b_log.png', thr=0.30)
render(16.0, 30.0, 40, 1200, True, 800, 2000, r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_b_log_soft.png')
render(16.0, 30.0, 0, 1200, False, 800, 2000, r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_b_lin.png', thr=0.25)
# whole file log
render(0.5, 30.0, 40, 1200, True, 600, 2200, r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_all_log.png', thr=0.3)
# seg A strokes
render(1.0, 15.0, 40, 1200, True, 800, 2000, r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_a_log.png', thr=0.25)