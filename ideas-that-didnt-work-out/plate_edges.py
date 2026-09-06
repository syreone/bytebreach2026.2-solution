import numpy as np
from PIL import Image

im = np.array(Image.open("plate.png").convert("L")).astype(float)
from scipy import ndimage
sx = ndimage.sobel(im, axis=1)
sy = ndimage.sobel(im, axis=0)
mag = np.hypot(sx, sy)

# threshold at ~ 90th percentile
thr = np.quantile(mag, 0.93)
print("thr:", thr)
edges = mag > thr

import sys
sys.path.insert(0, ".")
from ascii_render import ascii_render
print(ascii_render((edges*255).astype(np.uint8), width=160))