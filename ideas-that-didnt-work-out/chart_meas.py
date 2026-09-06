import numpy as np
from PIL import Image

im = Image.open('gallery.png').convert('RGB')
arr = np.array(im)
H, W = 1800, 1200
# chart area approx y 1560..1800
crop = im.crop((0, 1560, W, 1800))
crop.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\chart.png')
# measure columns: count non-white-ish pixel rows per x, find bar segments
import numpy as np
g = np.array(crop.convert('L')).astype(float)
# binary: dark pixels
dark = g < 128
colcount = dark.sum(axis=0)
rowcount = dark.sum(axis=1)
print("dark col profile nonzero xs:", np.where(colcount>0)[0][:5], "...", np.where(colcount>0)[0][-5:])
# find contiguous dark columns (bars) with gaps
xs = np.where(colcount > 2)[0]
groups = []
start = xs[0]; prev = xs[0]
for x in xs[1:]:
    if x - prev > 3:
        groups.append((start, prev))
        start = x
    prev = x
groups.append((start, prev))
print("groups x-ranges:", groups)
for g0, g1 in groups:
    seg = dark[:, g0:g1+1]
    rows = np.where(seg.sum(axis=1) > 0)[0]
    print("bar x %d..%d w=%d top=%d bot=%d h=%d" % (g0, g1, g1-g0+1, rows.min() if len(rows) else None, rows.max() if len(rows) else None, (rows.max()-rows.min()) if len(rows) else 0))
    # color of the bar
    col = arr[1700, g0+2, :] if False else None
# sample the RGB at mid-height of each bar x to get colors
for g0, g1 in groups:
    seg = dark[:, g0:g1+1]
    rows = np.where(seg.sum(axis=1) > 0)[0]
    if len(rows):
        mid = (rows.min()+rows.max())//2
        print("bar", g0, "mid rgb", arr[1560+mid, (g0+g1)//2, :])