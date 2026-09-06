from PIL import Image

im = Image.open("gallery.png").convert("L")
# exactly below bars (bars at x1019..1141), render at 1 char / pixel-ish
x0, y0, x1, y1 = 990, 985, 1190, 1270
region = im.crop((x0, y0, x1, y1))
tw, th = 100, 190
img = region.resize((tw, th), Image.LANCZOS)
px = img.load()
chars = " .:-=+*#%@"
for r in range(th):
    row = ""
    for c in range(tw):
        v = px[c, r]
        row += chars[min(9, v * 10 // 256)]
    print(row)
print()
print("region x%d-%d y%d-%d (col=%.1fpx row=%.1fpx)" % (x0, x1, y0, y1, (x1-x0)/tw, (y1-y0)/th))