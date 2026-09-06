from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("L")
a = np.array(im)
H, W = a.shape
# coarse 120x60 map over whole image
tw, th = 120, 60
img = a
px = np.array(im.resize((tw, th), Image.LANCZOS))
chars = " .:-=+*#%@"
for r in range(th):
    row = ""
    for c in range(tw):
        v = int(px[r, c])
        row += chars[min(9, v * 10 // 256)]
    print(row)
print("image %dx%d" % (W, H))