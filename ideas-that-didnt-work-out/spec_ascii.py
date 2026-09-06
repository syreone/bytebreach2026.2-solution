import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)
f, t, Sxx = signal.spectrogram(x, rate, nperseg=1024, noverlap=900)
S = 10*np.log10(Sxx + 1e-12)

def ascii_spect(t0, t1, fmin, fmax, log, rows, cols, path, pct_a=30, pct_b=99.5, invert=False):
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
    nt = Sb.shape[1]
    img = np.zeros((rows, nt))
    # map freq rows to image rows (row 0 = high freq)
    for i in range(len(fb)):
        r = int(round((1 - (idx[i]-lo)/(hi-lo)) * (rows-1)))
        img[r, :] = np.maximum(img[r, :], Sb[i, :])
    lo_p, hi_p = np.percentile(img, pct_a), np.percentile(img, pct_b)
    img = np.clip((img - lo_p)/(hi_p - lo_p + 1e-9), 0, 1)
    # downsample time cols
    steps = int(np.ceil(img.shape[1]/cols))
    if steps > 1:
        nt2 = (img.shape[1]//steps)*steps
        img = img[:, :nt2].reshape(rows, nt2//steps, steps).max(axis=2)
        if img.shape[1] < cols:
            pad = np.full((rows, cols-img.shape[1]), img.min())
            img = np.concatenate([img, pad], axis=1)
    # smooth lightly
    cm = " .:-=+*#%@"
    lines = []
    for r in range(rows):
        row = img[r, :]
        line = "".join(cm[min(int(row[c]*9.99), 9)] if row[c] > 0.01 else " " for c in range(cols))
        lines.append(line)
    open(path, 'w').write("\n".join(lines))
    print("wrote", path, "rows", rows, "cols", cols)

ascii_spect(0.5, 14.5, 150, 8000, True, 60, 180, r'C:\Users\Luka\AppData\Local\Temp\opencode\spA.txt')
ascii_spect(16.0, 30.0, 150, 8000, True, 60, 180, r'C:\Users\Luka\AppData\Local\Temp\opencode\spB.txt')
ascii_spect(16.0, 30.0, 150, 3000, True, 60, 180, r'C:\Users\Luka\AppData\Local\Temp\opencode\spB_low.txt')