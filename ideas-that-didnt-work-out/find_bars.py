from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.array(im)
r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)
bright = np.maximum(np.maximum(r,g),b)

for x in range(990, 1160):
    mask = (bright[:, x] > 200) & (sat[:, x] > 40)
    idx = np.where(mask)[0]
    if len(idx) and idx.max() in range(940, 1010):
        top_px = idx[idx < 900].min() if np.any(idx < 900) else idx.min()
        i = int(idx.max())
        print(x, "range[%d..%d] top=%d c=(%d,%d,%d)" % (int(idx.min()), i, int(top_px), r[i], g[i], b[i]))