from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img)
h, w, _ = arr.shape
print("image size:", w, h)

brightness = arr.sum(axis=2)
is_fg = brightness > 90

col_top = []
col_color = []
for x in range(w):
    ys = np.where(is_fg[:, x])[0]
    if len(ys) > 0 and (h - ys.min()) > 15:
        top_y = ys.min()
        sample_y = min(top_y + 8, h - 1)
        col_top.append(h - top_y)
        col_color.append(tuple(int(c) for c in arr[sample_y, x]))
    else:
        col_top.append(0)
        col_color.append((0, 0, 0))

def quantize(c, step=40):
    return tuple((v // step) * step for v in c)

qcolors = [quantize(c) for c in col_color]

bars = []
i = 0
while i < w:
    if qcolors[i] == (0, 0, 0):
        i += 1
        continue
    j = i
    while j < w and qcolors[j] == qcolors[i]:
        j += 1
    heights = col_top[i:j]
    if max(heights) > 15:
        avg_height = int(np.median([hh for hh in heights if hh > 0]))
        common_color = Counter(col_color[i:j]).most_common(1)[0][0]
        bars.append((i, j, avg_height, common_color))
    i = j

print(f"found {len(bars)} bars")
for idx, (x1, x2, height, color) in enumerate(bars):
    print(f"bar {idx+1}: x={x1}-{x2}, width={x2-x1}, height_px={height}, color={color}")
