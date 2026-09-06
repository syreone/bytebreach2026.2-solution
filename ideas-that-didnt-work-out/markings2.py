from PIL import Image

im = Image.open("gallery.png").convert("L")
x0, x1, y0, y1 = 560, 1175, 1055, 1185
crop = im.crop((x0, y0, x1, y1))
w, h = crop.size
px = crop.load()
for step in (1, 2):
    print("=== step", step, "dark<180 ===")
    for yy in range(0, h, step):
        line = ""
        for xx in range(w):
            v = px[xx, yy]
            # background cream ~214-224; glyph ~140-195; pure black 0
            if v < 180:
                line += "#"
            elif v < 205:
                line += "+"
            else:
                line += "."
        print(line)
    print()