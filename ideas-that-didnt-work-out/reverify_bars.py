from PIL import Image

im = Image.open("gallery.png").convert("RGB")
# find saturated columns: scan the chart region for vertical runs with hue≈colorset
xs = list(range(1019, 1142, 12))
print("bar scan")
heights = []
for i, x in enumerate(xs):
    top = None
    bot = None
    # scan y from 700 to 1150; bar = pixel with max channel>200 and min channel<170 (pastel saturated)
    for y in range(700, 1150):
        r, g, b = im.getpixel((x+1, y))
        mx, mn = max(r, g, b), min(r, g, b)
        if mx > 200 and (mx - mn) > 40:
            if top is None:
                top = y
            bot = y
    if top is None:
        # try scanning wider
        continue
    h = bot - top + 1
    heights.append(h)
    print("b%d top=%d bot=%d h=%d  h//3=%d(%s)" % (i+1, top, bot, h, h//3, chr(64+h//3) if h//3 <= 26 else "?"))
print("heights:", heights)

# also independent baseline check: find the row where all bars share a bottom
from collections import Counter
bottom_counts = Counter()
for i, x in enumerate(xs):
    top = None
    bot = None
    for y in range(700, 1150):
        r, g, b = im.getpixel((x+1, y))
        mx, mn = max(r, g, b), min(r, g, b)
        if mx > 200 and (mx - mn) > 40:
            if top is None: top = y
            bot = y
    bottom_counts[bot] += 1
print("most common bottoms:", bottom_counts.most_common(5))