import numpy as np
from scipy.io import wavfile
from scipy.ndimage import uniform_filter1d

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)

def rend(seg, name, cols=200, rows=36, thr_hi=0.85):
    # envelope: abs, then moving average 8ms
    win = int(rate*0.008)
    env = uniform_filter1d(np.abs(seg), win)
    # normalize to max
    m = env.max()
    env = env / m
    # downsample to cols
    n = len(env)
    steps = n // cols
    env2 = env[:steps*cols].reshape(cols, steps).max(axis=1)
    # rows via percentile to bring out shape
    lo, hi = np.percentile(env2, 30), np.percentile(env2, 99)
    v = np.clip((env2 - lo)/(hi-lo+1e-9), 0, 1)
    cm = " .:-=+*#%@"
    chars = ["".join(cm[min(int((1-v[c])*9.9),9)] for c in range(cols))]  # invert: light tall = letter
    # better: draw as vertical bars per time column: height ~ v
    lines = []
    for r in range(rows):
        line = ""
        for c in range(cols):
            h = int(v[c]* (rows-1))
            line += "@" if (rows-1-r) <= h else " "
        lines.append(line)
    open(name, 'w').write("\n".join(lines))
    print("wrote", name, "n", len(env))

rend(np.abs(L), r'C:\Users\Luka\AppData\Local\Temp\opencode\env_L.txt')
rend(np.abs(R), r'C:\Users\Luka\AppData\Local\Temp\opencode\env_R.txt')
rend(np.abs(L-R), r'C:\Users\Luka\AppData\Local\Temp\opencode\env_LR.txt')