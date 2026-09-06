from PIL import Image
import numpy as np

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img).astype(int)
h, w, _ = arr.shape

palette = [(255,192,192),(255,255,192),(192,255,192),
           (192,255,255),(192,192,255),(255,192,255)]

def closest_match(pixel, tol=40):
    for pc in palette:
        dist = sum((a-b)**2 for a, b in zip(pixel, pc)) ** 0.5
        if dist < tol:
            return pc
    return None

bar_ranges = [(53,57),(66,69),(78,81),(90,93),(102,105),(114,117),
              (126,129),(138,141),(150,153),(162,165),(174,177)]

print(f"measuring {len(bar_ranges)} bars")
for idx, (x1, x2) in enumerate(bar_ranges):
    mid_x = (x1 + x2) // 2
    is_match = [closest_match(tuple(arr[y, mid_x])) is not None for y in range(h)]

    # find the longest contiguous run of True
    best_start, best_len = 0, 0
    cur_start, cur_len = None, 0
    for y in range(h):
        if is_match[y]:
            if cur_start is None:
                cur_start = y
            cur_len += 1
            if cur_len > best_len:
                best_len = cur_len
                best_start = cur_start
        else:
            cur_start, cur_len = None, 0

    top_y = best_start
    bottom_y = best_start + best_len - 1
    height = bottom_y - top_y
    color = closest_match(tuple(arr[(top_y+bottom_y)//2, mid_x]))
    print(f"bar {idx+1}: x={x1}-{x2}, top_y={top_y}, bottom_y={bottom_y}, height_px={height}, color={color}")
