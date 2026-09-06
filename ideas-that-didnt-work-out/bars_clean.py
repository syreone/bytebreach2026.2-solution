from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.array(im)
r = a[:,:,0].astype(int); g = a[:,:,1].astype(int); b = a[:,:,2].astype(int)
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)
bright = np.maximum(np.maximum(r,g),b)

# find the 11 bars by scanning columns for tall bright-saturated runs that start near 745
print("axis candidate columns (bright & saturated, run starting ~<=760, ending ~996):")
bars = {}
for x in range(1000, 1160):
    col = ((bright[:, x] > 180) & (sat[:, x] > 50))
    # find runs in y 500..1050
    y = np.where(col[500:1060])[0] + 500
    if len(y) == 0:
        continue
    start, end = y.min(), y.max()
    runlen = end - start
    if runlen > 80 and y.min() < 770:
        start = int(start); end = int(end)
        bars[x] = (start, end)
        # color sample at a tall altitude
        cy = int(start + 60)
        print(x, "top=%d bottom=%d run=%d c=(%d,%d,%d)" % (start, end, end-start, int(r[cy,x]), int(g[cy,x]), int(b[cy,x])))

print("\nnum bar columns detected:", len(bars))