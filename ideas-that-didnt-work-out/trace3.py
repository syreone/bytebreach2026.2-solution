import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import median_filter

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)

f, t, Sxx = signal.spectrogram(x, rate, nperseg=512, noverlap=448)
S = 10*np.log10(Sxx + 1e-12)

fmin, fmax = 150.0, 7000.0
band = (f >= fmin) & (f <= fmax)
fb = f[band]
Sb = S[band, :]

# per column: pick lowest strong spectral peak above (colmax - 3dB) falloff starting from bottom
p40 = np.percentile(S, 40)
f0 = np.zeros(Sb.shape[1])
for i in range(Sb.shape[1]):
    col = Sb[:, i]
    cmax = col.max()
    thresh = max(cmax - 4.0, p40)
    cand = np.where(col > thresh)[0]
    if len(cand):
        f0[i] = fb[cand[0]]
    else:
        f0[i] = 0.0

f0s = median_filter(f0, size=7)
f0s[f0s < fmin] = fmin
f0s[f0s > fmax] = fmax

def render(tt, ff, base, path, wide=400, H=64):
    m = (t >= tt[0]) & (t <= tt[1])
    tr = np.full((H, int(wide)), 1.0)
    xp = np.linspace(0, wide-1, m.sum())
    loglo, loghi = np.log10(fmin), np.log10(fmax)
    y = 1 - (np.log10(ff[m]) - loglo)/(loghi - loglo)
    xi = 0
    for i in range(m.sum()):
        col = int(round(xp[i]))
        r = int(round(y[i].item() * (H-1)))
        if 0 <= r < H and tr[r, col] == 1.0:
            for d in range(-1, 2):
                rr = r + d
                if 0 <= rr < H:
                    tr[rr, col] = 0.5
            tr[r, col] = 0.0
    # stretch contrast
    g = (tr - tr.min())/(tr.max()-tr.min()+1e-9)
    cm = " .:-=+*#%@"
    lines = ["".join(cm[min(int((1-g[r,c])*9.99), 9)] for c in range(wide)) for r in range(H)]
    open(path, 'w').write("\n".join(lines))
    Image.fromarray((tr*255).astype(np.uint8)).resize((wide*3, H*3), Image.LANCZOS).save(base)
    print("saved", base, path)

from PIL import Image
render((0.0, 30.0), f0s, r'C:\Users\Luka\AppData\Local\Temp\opencode\trace_all.png', r'C:\Users\Luka\AppData\Local\Temp\opencode\trace_all.txt')
render((1.0, 15.0), f0s, r'C:\Users\Luka\AppData\Local\Temp\opencode\trace_A.png', r'C:\Users\Luka\AppData\Local\Temp\opencode\trace_A.txt')
render((16.0, 30.0), f0s, r'C:\Users\Luka\AppData\Local\Temp\opencode\trace_B.png', r'C:\Users\Luka\AppData\Local\Temp\opencode\trace_B.txt')