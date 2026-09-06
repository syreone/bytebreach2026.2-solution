from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.asarray(im).astype(int)

def render(x0, y0, x1, y1, out, sx=1, sy=1):
    lines = []
    for y in range(y0, y1, sy):
        s = []
        for x in range(x0, x1, sx):
            r, g, b = a[y, x]
            lum = (r + g + b) // 3
            if lum > 225:
                s.append(" ")
            elif lum < 90:
                s.append("#")
            else:
                s.append(".")
        lines.append("".join(s))
    open(out, "w").write("\n".join(lines))

render(0, 1500, 620, 1650, r"C:\Users\Luka\AppData\Local\Temp\opencode\caption_full.txt")
render(0, 1500, 620, 1595, r"C:\Users\Luka\AppData\Local\Temp\opencode\caption_tight.txt")
print("ok")