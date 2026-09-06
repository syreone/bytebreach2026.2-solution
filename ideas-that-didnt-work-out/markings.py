from PIL import Image, ImageOps

im = Image.open("gallery.png").convert("RGB")
# rasterize the region below the bars where gray marking appeared
x0, x1, y0, y1 = 560, 1175, 1055, 1185
crop = im.crop((x0, y0, x1, y1)).convert("L")
w, h = crop.size
# invert: mark "dark" pixels (gray glyphs on light bg) - use threshold
g = crop.point(lambda v: 255 if v < 130 else 0)
g.save("markings_bin.png")
# ascii render every 2nd y
arr = g.load()
for yy in range(0, h, 2):
    line = "".join("#" if arr[xx, yy] == 0 else "." for xx in range(w))
    print("%4d %s" % (y0+yy, line))
print()
# OCR version (grayscale upscaled)
g2 = crop.resize((crop.width*4, crop.height*4), Image.LANCZOS)
g2.save("markings_4x.png")