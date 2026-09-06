from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img)
h, w, _ = arr.shape
print("image size:", w, h)

brightness = arr.sum(axis=2)
is_fg = brightness > 90

# per-column: does it have a real bar, and how tall is it
col_has_bar = []
col_top = []
for x in range(w):
    ys = np.where(is_fg[:, x])[0]
    if len(ys) > 0 and (h - ys.min()) > 40:  # real bar, not noise
        col_has_bar.append(True)
        col_top.append(ys.min())
    else:
        col_has_bar.append(False)
        col_top.append(None)

# group consecutive True columns into bars (position-based, ignores color)
bars = []
i = 0
while i < w:
    if not col_has_bar[i]:
        i += 1
        continue
    j = i
    while j < w and col_has_bar[j]:
        j += 1
    bars.append((i, j))
    i = j

print(f"found {len(bars)} bar groups")

for idx, (x1, x2) in enumerate(bars):
    mid_x = (x1 + x2) // 2
    top_y = col_top[mid_x]
    height = h - top_y
    # sample color from well inside the bar, away from top edge antialiasing
    sample_y = min(top_y + (h - top_y) // 2, h - 1)
    colors_in_bar = [tuple(int(c) for c in arr[sample_y, x]) for x in range(x1, x2)]
    common_color = Counter(colors_in_bar).most_common(1)[0][0]
    print(f"bar {idx+1}: x={x1}-{x2}, width={x2-x1}, height_px={height}, color={common_color}")
