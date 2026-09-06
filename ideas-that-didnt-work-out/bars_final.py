from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.array(im)
r = a[:,:,0].astype(int); g = a[:,:,1].astype(int); b = a[:,:,2].astype(int)
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)

# for each column, find the bright bar region above y=1050
# bars: tall colored blocks with baseline at ~996, tops vary
results = []
for x in range(1000, 1150):
    # bright saturated pixels in y 600..1000 (the bar blocks)
    mask = (sat[:, x] > 50) & (np.maximum(np.maximum(r[:,x], g[:,x]), b[:,x]) > 150)
    idx = np.where(mask[600:1010])[0] + 600
    if len(idx) > 20:
        results.append((x, int(idx.min()), int(idx.max()), len(idx)))

# group into bars (12px pitch)
if not results:
    print("no bars found")
else:
    print("bar columns found: %d total" % len(results))
    # find the top of each bar at each x: first saturated pixel above y=850
    bar_tops = {}
    for x in range(1000, 1150):
        mask = (sat[:, x] > 50) & (np.maximum(np.maximum(r[:,x], g[:,x]), b[:,x]) > 150)
        idx = np.where(mask[700:1000])[0] + 700
        if len(idx) > 5:
            bar_tops[x] = int(idx.min())

    # group contiguous columns
    if bar_tops:
        prev_x = -10
        bars = []
        cur_bar_xs = []
        for x in sorted(bar_tops.keys()):
            if x - prev_x > 1:
                if cur_bar_xs:
                    avg_top = int(np.mean([bar_tops[x2] for x2 in cur_bar_xs]))
                    bars.append((cur_bar_xs[0], cur_bar_xs[-1], avg_top))
                cur_bar_xs = [x]
            else:
                cur_bar_xs.append(x)
            prev_x = x
        if cur_bar_xs:
            avg_top = int(np.mean([bar_tops[x2] for x2 in cur_bar_xs]))
            bars.append((cur_bar_xs[0], cur_bar_xs[-1], avg_top))

        print("\n%d bars detected:" % len(bars))
        for i, (x0, x1, top) in enumerate(bars):
            h = 996 - top  # baseline is 996
            letter = chr(h // 3) if 64 < h // 3 < 123 else "?"
            print("  bar %2d: x=%d..%d  top=%d  h=%3d  h/3=%2d  char=%s" % (i+1, x0, x1, top, h, h//3, letter))

        word = ""
        for _, _, top in bars:
            h = 996 - top
            c = chr(h // 3) if 64 < h // 3 < 123 else "?"
            word += c
        print("\nword:", word)