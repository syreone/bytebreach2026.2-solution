import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import median_filter

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)

b, a = signal.butter(4, 200.0/(rate/2), 'high')
xh = signal.filtfilt(b, a, x)

f, t, Sxx = signal.spectrogram(xh, rate, nperseg=1024, noverlap=900)
S = 10*np.log10(Sxx + 1e-12)

fmin, fmax = 200.0, 6000.0
band = (f >= fmin) & (f <= fmax)
fb = f[band]
Sb = S[band, :]

colmax = Sb.max(axis=0)
thresh = np.maximum(colmax - 6.0, np.percentile(S[band], 30))
strong = Sb > thresh[None, :]
first = np.argmax(strong, axis=0)  # first True row index per column
ok = strong.any(axis=0)
f0 = np.where(ok, fb[first], fmin)
f0s = median_filter(f0, size=9)
np.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\f0_high.npy', np.vstack([t, f0s]))
for name, t0, t1 in [('A', 1.0, 15.0), ('B', 16.0, 30.0)]:
    m = (t >= t0) & (t <= t1)
    v = f0s[m]
    print(name, "pcts", np.percentile(v, [5,25,50,75,95]), "min %.1f max %.1f" % (v.min(), v.max()))
print("n bins", len(t))