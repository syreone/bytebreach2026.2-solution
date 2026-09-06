from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img).astype(int)
h, w, _ = arr.shape

brightness = arr.max(axis=2)
is_fg = brightness > 90

bar_ranges = [(53,57),(66,69),(78,81),(90,93),(102,105),(114,117),
              (126,129),(138,141),(150,153),(162,165),(174,177)]

print(f"measuring {len(bar_ranges)} bars")
for idx, (x1, x2) in enumerate(bar_ranges):
    mid_x = (x1 + x2) // 2
    col = is_fg[:, mid_x]
    # scan upward from the bottom of the image, stop at first gap
    y = h - 1
    while y >= 0 and not col[y]:
        y -= 1
    bottom_y = y
    while y >= 0 and col[y]:
        y -= 1
    top_y = y + 1
    height = bottom_y - top_y
    sample_y = (top_y + bottom_y) // 2
    colors_in_bar = [tuple(arr[sample_y, x]) for x in range(x1, x2)]
    common_color = Counter(colors_in_bar).most_common(1)[0][0]
    print(f"bar {idx+1}: x={x1}-{x2}, top_y={top_y}, bottom_y={bottom_y}, height_px={height}, color={common_color}")
