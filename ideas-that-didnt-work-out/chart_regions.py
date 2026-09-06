from PIL import Image

im = Image.open("gallery.png")
# chart x618-1147, y above chart, below chart, and to the right
regions = {
    "chart_above":  (600, 680, 1200, 750),
    "chart_below":  (500, 1540, 1200, 1650),
    "chart_right":  (1100, 700, 1200, 1565),
    "chart_left":   (500, 700, 650, 1565),
    "chart_center": (650, 800, 1100, 1010),
    "gallery_full": (0, 0, 1200, 1800),
}
for name, box in regions.items():
    crop = im.crop(box).convert("L")
    crop = crop.resize((crop.width*3, crop.height*3), Image.LANCZOS)
    out = "crop_%s.png" % name
    crop.save(out)
    print(name, box, crop.size)