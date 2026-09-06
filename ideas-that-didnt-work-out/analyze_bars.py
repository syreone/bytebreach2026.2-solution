from PIL import Image
import numpy as np

img = Image.open('chart_crop3.png').convert('RGB')
arr = np.array(img)
h, w, _ = arr.shape

# a pixel counts as "bar" if it's not black/near-black background
brightness = arr.sum(axis=2)
is_bar = brightness > 60  # tweak threshold if needed

# for each column, find the topmost bar pixel (smaller y = taller bar)
col_top = []
col_color = []
for x in range(w):
    ys = np.where(is_bar[:, x])[0]
    if len(ys) > 0:
        top_y = ys.min()
        col_top.append(top_y)
        # sample color a bit below the top, to avoid anti-aliased edge pixels
        sample_y = min(top_y + 5, h - 1)
        col_color.append(tuple(arr[sample_y, x]))
    else:
        col_top.append(None)
        col_color.append(None)

# group consecutive non-None columns into "bars"
bars = []
current = []
for x in range(w):
    if col_top[x] is not None:
        current.append((x, col_top[x], col_color[x]))
    else:
        if current:
            bars.append(current)
            current = []
if current:
    bars.append(current)

print(f"found {len(bars)} bar groups")
for i, bar in enumerate(bars):
    xs = [p[0] for p in bar]
    tops = [p[1] for p in bar]
    colors = [p[2] for p in bar]
    # use median top and most common color for stability
    med_top = int(np.median(tops))
    height = h - med_top
    # most common color (mode)
    from collections import Counter
    common_color = Counter(colors).most_common(1)[0][0]
    print(f"bar {i+1}: x={xs[0]}-{xs[-1]}, height_px={height}, color={common_color}")
