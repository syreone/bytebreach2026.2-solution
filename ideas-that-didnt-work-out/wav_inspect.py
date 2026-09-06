import numpy as np
from scipy.io import wavfile

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)
n = len(L)
diff = np.abs(L - R)
print("rate:", rate, "samples:", n, "dur:", n/rate)
print("L==R fraction:", (diff==0).mean())
print("diff > 1 fraction:", (diff>1).mean())
print("diff > 100 fraction:", (diff>100).mean())
# where do they differ? by sample index
big = diff > 100
idx = np.nonzero(big)[0]
if idx.size:
    print("big-diff sample range:", idx.min(), idx.max(), "(t %.2f - %.2f s)" % (idx.min()/rate, idx.max()/rate))
# amplitude stats
print("L range:", L.min(), L.max())
print("R range:", R.min(), R.max())
# RMS per second
import numpy as np
sec = int(rate)
for s in range(0, n, sec):
    seg = L[s:s+sec]
    print("t %4d s  rms %9.1f  peak %9.1f" % (s/rate, np.sqrt((seg**2).mean()), np.abs(seg).max()))