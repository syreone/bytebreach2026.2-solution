from PIL import Image
im = Image.open("gallery.png").convert("RGB")
crops = []
for x0 in (0, 600):
    for y0 in (0, 600, 900, 1200, 1500, 1650):
        x1 = min(x0 + 600, 1200)
        y1 = min(y0 + 300, 1800)
        if im.crop((x0, y0, x1, y1)).size[0] > 0:
            im.crop((x0, y0, x1, y1)).resize((int(2 * (x1 - x0)), int(2 * (y1 - y0))), Image.LANCZOS).save(
                rf"C:\Users\Luka\AppData\Local\Temp\opencode\strip_{x0}_{y0}.png")
            crops.append((x0, y0))
print(crops)