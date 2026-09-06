import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

im = np.array(Image.open("plate.png").convert("L")).astype(float)
H, W = im.shape

# picture bbox from comp: x186-1423, y294-942
strips = {
    "top":   (186, 292, 1423, 344),
    "bot":   (186, 892, 1423, 944),
    "left":  (140, 294, 190, 942),
    "right": (1417, 294, 1480, 942),
}

from scipy import ndimage as ndi
for name, (x0,y0,x1,y1) in strips.items():
    crop = im[y0:y1, x0:x1]
    blur = ndi.gaussian_filter(crop, 6)
    hi = crop - blur          # carved: local deviations
    # scale to 0-255
    s = np.percentile(hi, 2), np.percentile(hi, 98)
    norm = np.clip((hi - s[0])/(s[1]-s[0])*255, 0, 255).astype(np.uint8)
    Image.fromarray(norm).save("carve_%s.png" % name)
    # render ASCII of the carve result
    img = norm
    h, w = img.shape
    width = min(400, w)
    height = max(1, int(round(h*width/w*0.5)))
    rimg = Image.fromarray(img).resize((width, height))
    g = np.array(rimg).astype(float)
    g = (g-g.min())/(g.max()-g.min())
    cm = "@%#*+=-:. "
    rows = ["".join(cm[int(g[r,c]*9)] for c in range(width)) for r in range(height)]
    open("carve_%s.txt" % name, "w").write("\n".join(rows))
    print(name, "crop", w, h, "-> render", width, height)

print("saved carve strips")