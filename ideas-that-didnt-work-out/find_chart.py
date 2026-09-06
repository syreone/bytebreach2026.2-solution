from PIL import Image
import numpy as np

arr = np.array(Image.open('gallery.png').convert('RGB')).astype(int)
h, w, _ = arr.shape
palette = np.array([(255,192,192),(255,255,192),(192,255,192),
                    (192,255,255),(192,192,255),(255,192,255)])

d = np.sqrt(((arr[:,:,None,:] - palette[None,None,:,:])**2).sum(axis=3))
mind = d.min(axis=2)
mask = mind < 45
print("matches:", mask.sum())
ys, xs = np.where(mask)
print("bbox x:", xs.min() if len(xs) else None, xs.max() if len(xs) else None, "y:", ys.min() if len(ys) else None, ys.max() if len(ys) else None)

# per-column runs
colruns = np.where(mask, 1, 0).sum(axis=0)
filled = colruns > 10
segs = []
i = 0
while i < w:
    if not filled[i]:
        i += 1; continue
    j = i
    while j < w and filled[j]:
        j += 1
    segs.append((i, j)); i = j
print("column segments:", segs[:40])

# for each segment, find top of colored area in that column range
for (x1, x2) in segs:
    sub = mask[:, x1:x2]
    rows = np.where(sub.sum(axis=1) > 0)[0]
    if len(rows):
        print("seg x %d..%d  ytop=%d ybot=%d h=%d" % (x1, x2, rows.min(), rows.max(), rows.max()-rows.min()+1))
        midx = (x1+x2)//2
        ymid = (rows.min()+rows.max())//2
        col = arr[ymid, midx]
        print("   mid rgb", col)