import numpy as np
from scipy.io import wavfile
from scipy import signal
from PIL import Image

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)

# Params tuned: 2048 window shows sweeps nicely
f, t, Sxx = signal.spectrogram(L, rate, nperseg=2048, noverlap=1792)
S = 10*np.log10(Sxx + 1e-12)
print("bins", len(f), "windows", len(t), "frange", f[0], f[-1], "t windows/s", rate/256)

def show(lo, hi, name, fmax=6000, label_rows=46, chars_per_win=0.8):
    # crop freq 0..fmax
    fsel = f <= fmax
    Ss = S[fsel, lo:hi]
    fr = f[fsel]
    # map rows: log scale from 100Hz to fmax
    logf = np.log10(np.clip(fr, 60, None))
    rows = np.linspace(logf.min(), logf.max(), label_rows)
    img = np.zeros((label_rows, Ss.shape[1]), dtype=np.uint8)
    for i in range(label_rows-1):
        m = (logf >= rows[i]) & (logf < rows[i+1])
        if m.sum():
            img[i] = Ss[m].max(axis=0)
    # threshold/normalize
    imgf = img.astype(float)
    lo_, hi_ = np.percentile(imgf, 20), np.percentile(imgf, 99.5)
    imgf = np.clip((imgf - lo_)/(hi_-lo_)*255, 0, 255)
    # downsample time to width
    width = int(Ss.shape[1]*chars_per_win)
    im = Image.fromarray(imgf.astype(np.uint8)).resize((width, label_rows), Image.LANCZOS)
    g = np.array(im).astype(float)
    g = (g-g.min())/(g.max()-g.min()+1e-9)
    cm = " .:-=+*#%@"
    lines = ["".join(cm[min(int(g[r,c]*10),9)] for c in range(width)) for r in range(label_rows)]
    open("%s.txt" % name, "w").write("\n".join(lines))
    print("%s: t %.2f-%.2f s, windows %d-%d, width %d" % (name, lo/187.5, hi/187.5, lo, hi, width))

# segA: strokes 1..13s
show(190, 2500, "specA")
# segB: pass 16..30s
show(3000, 5622, "specB")
# whole
show(0, 5622, "specAll")