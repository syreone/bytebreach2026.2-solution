import numpy as np
from scipy.io import wavfile
from scipy import ndimage

rate, data = wavfile.read('vault.wav')
L = data[:,0].astype(np.float64)
R = data[:,1].astype(np.float64)

def build(lo, hi, wx, hy, xr, yr):
    x = L[lo:hi]; y = R[lo:hi]
    cols = np.clip(((x - xr[0])/(xr[1]-xr[0])*(wx-1)).astype(int), 0, wx-1)
    rows = np.clip(((y - yr[0])/(yr[1]-yr[0])*(hy-1)).astype(int), 0, hy-1)
    img = np.zeros((hy, wx), dtype=np.uint8)
    np.add.at(img, (rows, cols), 1)
    return img >= 1

img = build(16*rate, 30*rate, 300, 150, (-32000,32000), (-21000,21000))
lab, n = ndimage.label(img)
sizes = ndimage.sum(img, lab, range(1, n+1))
objs = ndimage.find_objects(lab)

def render_comp(sl):
    crop = img[sl]
    h = crop.shape[0]; w = crop.shape[1]
    if w > 100:
        # scale down x2
        from scipy import ndimage as ndi
        k = max(1, w//80)
        crop = crop[::k, ::k]
    lines = []
    for rr in range(crop.shape[0]-1, -1, -1):
        lines.append("".join("#" if v else "." for v in crop[rr]))
    return "\n".join(lines)

lst = []
for i in range(1, n+1):
    sl = objs[i-1]
    lst.append((sizes[i-1], sl))
lst.sort(key=lambda t: t[1][1].start)
for s, sl in lst:
    print("="*30)
    print("comp size", s, "bbox x", sl[1].start, sl[1].stop-1, "y", sl[0].start, sl[0].stop-1)
    print(render_comp(sl))