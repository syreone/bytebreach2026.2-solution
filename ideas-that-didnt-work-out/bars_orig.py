from PIL import Image
import numpy as np

arr = np.array(Image.open('gallery.png').convert('RGB')).astype(int)
palette = np.array([(255,192,192),(255,255,192),(192,255,192),
                    (192,255,255),(192,192,255),(255,192,255)])
d = np.sqrt(((arr[:,:,None,:] - palette[None,None,:,:])**2).sum(axis=3))
mind = d.min(axis=2)
which = d.argmin(axis=2)
mask = mind < 8

region = (600, 700, 1200, 1650)
mx, my, Mx, My = region
sub = mask[my:My, mx:Mx]
w = sub.shape[1]

colcnt = sub.sum(axis=0)
filled = colcnt > 15
segs = []
i = 0
while i < w:
    if not filled[i]:
        i += 1; continue
    j = i
    while j < w and filled[j]:
        j += 1
    segs.append((i, j)); i = j
print("bar column segments (relative x):", segs)

bars = []
for (a, b) in segs:
    cols = sub[:, a:b]
    rows = np.where(cols.sum(axis=1) > 0)[0]
    if len(rows) == 0:
        continue
    top = rows.min(); bot = rows.max()
    midx = (a+b)//2
    midy = (top+bot)//2
    col = palette[which[my+midy, mx+midx]]
    bars.append((mx+a, mx+b, my+top, my+bot, tuple(col)))
for b in bars:
    x1, x2, t, bo, c = b
    print("x %d..%d  ytop %d ybot %d h=%d midcolor %s" % (x1, x2, t, bo, bo-t+1, c))

# also detect a baseline / axis: find dark line below bars
# check region below y 1565 up to 1650 for dark horizontal line in x 600-1200
g = np.array(Image.open('gallery.png').convert('L')).astype(int)
dark = g < 100
for y in range(1560, 1650):
    cnt = dark[y, 600:1200].sum()
    if cnt > 400:
        print("dark horizontal segment at y=%d count=%d" % (y, cnt))