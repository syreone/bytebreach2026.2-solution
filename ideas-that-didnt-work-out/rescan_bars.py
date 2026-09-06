from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.asarray(im).astype(int)

sat = a.max(axis=2) - a.min(axis=2)
mask = (sat > 60) & (a.min(axis=2) < 200)
sat_bright = a.max(axis=2) > 120

# vertical runs per column of saturated color
x0, x1, y0, y1 = 600, 1200, 600, 1150
cols = {}
for x in range(x0, x1):
    runs = []
    on = False
    start = 0
    for y in range(y0, y1):
        m = mask[y, x] and sat_bright[y, x]
        if m and not on:
            on, start = True, y
        elif not m and on:
            on = False
            if y - start >= 30:
                runs.append((start, y - 1))
    if runs:
        cols[x] = runs

# group contiguous columns with same run signature
groups = []
if cols:
    xs = sorted(cols)
    cur = [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] == 1:
            cur.append(x)
        else:
            groups.append((cur[0], cur[-1], cols[cur[0]]))
            cur = [x]
    groups.append((cur[0], cur[-1], cols[cur[0]]))

for g in groups:
    xa, xb, runs = g
    h = runs[-1][1] - runs[0][0] + 1
    r, gg, b = a[runs[0][0] + 5, (xa + xb) // 2]
    print(f"bar x {xa}-{xb}: top {runs[0][0]}, bottom {runs[-1][1]}, h {h}, color(rgb) {tuple(a[runs[0][0]+1,(xa+xb)//2])}")