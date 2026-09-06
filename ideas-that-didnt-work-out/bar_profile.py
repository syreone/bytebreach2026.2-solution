from PIL import Image
im = Image.open("gallery.png").convert("RGB")
x = 1020  # bar1 column
prev = None
print("y    RGB")
for y in range(700, 1120, 8):
    r, g, b = im.getpixel((x, y))
    print("%3d  (%3d,%3d,%3d)" % (y, r, g, b))
print()
# also bar top sliver at 1px granularity near boundaries
for y0 in (738, 745, 752, 990, 995, 1000, 1074, 1080, 1086):
    r, g, b = im.getpixel((x, y0))
    print("x=1020 y=%3d (%3d,%3d,%3d)" % (y0, r, g, b))