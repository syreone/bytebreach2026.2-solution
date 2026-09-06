from PIL import Image, ImageOps, ImageFilter

im = Image.open("gallery.png").convert("L")
regions = {
 "below_base": (940, 995, 1175, 1120),
 "above_base": (600, 700, 1175, 995),
}
for name, box in regions.items():
    c = im.crop(box)
    # crop only pixels that look "ink" (dark) to boost
    g = c.point(lambda v: 255 if v > 150 else 0)
    g = g.resize((g.width*4, g.height*4), Image.LANCZOS)
    g.save("axis_%s.png" % name)
    print(name, g.size)