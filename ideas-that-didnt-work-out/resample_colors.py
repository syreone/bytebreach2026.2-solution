from PIL import Image

im = Image.open("gallery.png").convert("RGB")
# bar x positions from earlier scan: x1019-1141 at 12px spacing, 2px wide
xs = list(range(1019, 1142, 12))
print("bar xs:", xs, "count", len(xs))
for i, x in enumerate(xs):
    # sample several points along the bar to get color run
    for y in (1030, 1080, 1130, 1180, 1230, 1280):
        px = im.getpixel((x+1, y))
        print("  b%d y%d" % (i+1, y), px)
    print()