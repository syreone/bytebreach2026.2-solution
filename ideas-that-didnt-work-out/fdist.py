import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, data = wavfile.read('vault.wav')
x = data[:,0].astype(np.float64)
f, t, Sxx = signal.spectrogram(x, rate, nperseg=512, noverlap=448)
S = 10*np.log10(Sxx + 1e-12)
print("f range", f[0], f[-1], len(f))
for name, t0, t1 in [('A', 1.0, 15.0), ('B', 16.0, 30.0)]:
    m = (t >= t0) & (t <= t1)
    am = np.argmax(S[:, m], axis=0)
    vals = f[am]
    print("== ", name, "argmax freq percentiles:", np.percentile(vals, [5,25,50,75,95]), "min", vals.min(), "max", vals.max())
    # count frac below 1000
    print("   frac<1000Hz:", (vals < 1000).mean(), " frac<300:", (vals < 300).mean(), " frac<2000:", (vals<2000).mean())
# also whole
am = np.argmax(S, axis=0)
print("ALL argmax pcts:", np.percentile(f[am], [5,25,50,75,95]))
# what fraction of columns have max freq in typical bin ranges
h, _ = np.histogram(f[am], bins=np.arange(0, 8000, 100))
print("hist of argmax f (0..8000, 100Hz bins):", h)
import scipy.stats as st
print("mode freq:", f[st.mode(am, axis=None).mode])