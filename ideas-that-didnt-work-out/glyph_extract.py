import numpy as np
from scipy.io import wavfile
from scipy import ndimage
from PIL import Image

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)

def glyphs(lo, hi, wx, hy, xr, yr, name, minpx=3):
    x = L[lo:hi]; y = R[lo:hi]
    cols = np.clip(((x - xr[0])/(xr[1]-xr[0])*(wx-1)).astype(int), 0, wx-1)
    rows = np.clip(((y - yr[0])/(yr[1]-yr[0])*(hy-1)).astype(int), 0, hy-1)
    img = np.zeros((hy, wx), dtype=np.uint8)
    np.add.at(img, (rows, cols), 1)
    binm = (img >= 1)
    lab, n = ndimage.label(binm)
    print(name, "components:", n)
    sizes = ndimage.sum(binm, lab, range(1, n+1))
    # bboxes per comp
    objs = ndimage.find_objects(lab)
    lst = []
    for i in range(n):
        if sizes[i] < minpx: continue
        sl = objs[i]
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        lst.append((sizes[i], i, sl, w, h))
    lst.sort(key=lambda t: t[2][1].start)
    for s, i, sl, w, h in lst:
        print("  comp %d size %d bbox x %d-%d y %d-%d" % (i, s, sl[1].start, sl[1].stop-1, sl[0].start, sl[0].stop-1))
    return img, binm, lst

# segB continuous pass
img, binm, lst = glyphs(16*rate, 30*rate, 300, 150, (-32000,32000), (-21000,21000), "segB")
Im = Image.fromarray(binm.astype(np.uint8)*255)
Im.save("segB_bin.png")
print("saved segB_bin.png")
# Save per-component crops magnified
for s, i, sl, w, h in lst:
    crop = (binm*255)[sl]
    im = Image.fromarray(crop)
    im = im.resize((max(1,w*4), max(1,h*4)), Image.NEAREST)
    im.save("glyph_%02d_%02dx%02d.png" % (i, w, h))
print("saved glyph crops")