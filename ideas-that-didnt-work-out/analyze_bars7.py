from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img).astype(int)
h, w, _ = arr.shape
print("image size:", w, h)

brightness = arr.max(axis=2)
is_fg = brightness > 90

# blank out just the thin top border row(s) and bottom gold trim row(s),
# WITHOUT cropping - keep full height so real bar tops aren't clipped
is_fg[0:10, :] = False       # top border strip
is_fg[390:410, :] = False    # bottom gold trim strip

# known bar x-ranges from previous consistent detection
bar_ranges = [(53,57),(66,69),(78,81),(90,93),(102,105),(114,117),
              (126,129),(138,141),(150,153),(162,165),(174,177)]

print(f"measuring {len(bar_ranges)} bars")
for idx, (x1, x2) in enumerate(bar_ranges):
    mid_x = (x1 + x2) // 2
    ys = np.where(is_fg[:, mid_x])[0]
    if len(ys) == 0:
        print(f"bar {idx+1}: no pixels found")
        continue
    top_y = ys.min()
    bottom_y = ys.max()
    height = bottom_y - top_y
    sample_y = (top_y + bottom_y) // 2
    colors_in_bar = [tuple(arr[sample_y, x]) for x in range(x1, x2)]
    common_color = Counter(colors_in_bar).most_common(1)[0][0]
    print(f"bar {idx+1}: x={x1}-{x2}, top_y={top_y}, bottom_y={bottom_y}, height_px={height}, color={common_color}")
