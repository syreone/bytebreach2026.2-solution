from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.array(im)
r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)
bright = np.maximum(np.maximum(r,g),b)

# global scan: for each column x, count bright-saturated pixels between y500 and y1200
print("image size", a.shape)
hits = []
for x in range(0, a.shape[1]):
    mask = (bright[:, x] > 200) & (sat[:, x] > 40)
    idx = np.where(mask)[0]
    if len(idx) > 100:
        hits.append((x, int(idx.min()), int(idx.max()), int(len(idx))))
print("cols with >100 bright-sat px in [y500..]:")
for h in hits:
    if h[1] > 400:
        print(h)