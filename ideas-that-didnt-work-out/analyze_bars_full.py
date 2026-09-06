from PIL import Image
import numpy as np

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img).astype(int)
h, w, _ = arr.shape

palette = [(255,192,192),(255,255,192),(192,255,192),
           (192,255,255),(192,192,255),(255,192,255)]

def closest_match(pixel, tol=45):
    best = None
    best_dist = 999
    for pc in palette:
        dist = sum((a-b)**2 for a, b in zip(pixel, pc)) ** 0.5
        if dist < tol and dist < best_dist:
            best = pc
            best_dist = dist
    return best

# scan every column for a match, not just known ranges
col_match = []
for x in range(w):
    is_match = [closest_match(tuple(arr[y, x])) is not None for y in range(h)]
    best_start, best_len = 0, 0
    cur_start, cur_len = None, 0
    for y in range(h):
        if is_match[y]:
            if cur_start is None: cur_start = y
            cur_len += 1
            if cur_len > best_len:
                best_len, best_start = cur_len, cur_start
        else:
            cur_start, cur_len = None, 0
    col_match.append((best_start, best_len))

# group into bars by any column with a real run (len > 15)
bars = []
i = 0
while i < w:
    if col_match[i][1] <= 15:
        i += 1
        continue
    j = i
    while j < w and col_match[j][1] > 15:
        j += 1
    bars.append((i, j))
    i = j

print(f"found {len(bars)} bars total (full width scan)")
for idx, (x1, x2) in enumerate(bars):
    mid = (x1+x2)//2
    top, length = col_match[mid]
    color = closest_match(tuple(arr[top+length//2, mid]))
    print(f"bar {idx+1}: x={x1}-{x2}, height_px={length}, color={color}")
