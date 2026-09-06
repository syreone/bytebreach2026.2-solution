from PIL import Image

im = Image.open("gallery.png").convert("L")
# whole bottom area: y900..1260, full width
W, H = im.size
x0, y0, x1, y1 = 0, 900, W, 1260
region = im.crop((x0, y0, x1, y1))
# downsample to readable ASCII
tw, th = 160, 100
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
print("region: x%d-%d  y%d-%d  (each ascii col = %.1f px, row = %.1f px)" % (x0, x1, y0, y1, (x1-x0)/tw, (y1-y0)/th))