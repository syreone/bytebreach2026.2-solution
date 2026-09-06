import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)

for ch, name in [(L,"L"), (R,"R")]:
    f, t, Sxx = signal.spectrogram(ch, rate, nperseg=1024, noverlap=768)
    # Sxx is log power; normalize
    S = 10*np.log10(Sxx + 1e-12)
    # summary via ASCII: downsample to ~200 cols x 60 rows
    import sys
    sys.path.insert(0, ".")
    from ascii_render import ascii_render
    img = (S - S.min()) / (S.max() - S.min())
    img8 = (img*255).astype(np.uint8)
    from PIL import Image
    im = Image.fromarray(img8)
    print("== spectrogram %s freq %d-%d Hz, bins %d, time %d windows" % (name, f[0], f[-1], len(f), len(t)))
    print(ascii_render(img8, width=160, invert=True, charmap=" .:-=+*#%@"))