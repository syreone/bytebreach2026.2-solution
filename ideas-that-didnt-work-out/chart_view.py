from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.asarray(im)

def render(x0, y0, x1, y1, out, scale=3, step=3, chars=" .:-=+*#%@"):
    arr = a[y0:y1, x0:x1].astype(int)[::step, ::scale]
    lines = []
    for row in arr:
        s = []
        for px in row:
            r, g, b = px
            d = max(r - g, g - b) + max(r, b) - min(r, b)
            lum = (r + g + b) // 3
            if r > 230 and g > 230 and b > 230:
                ch = " "
            elif lum < 40:
                ch = "#"
            elif d > 60 or lum < 90:
                ch = "@"
            else:
                ch = "."
            s.append(ch)
        lines.append("".join(s))
    with open(out, "w") as f:
        f.write("\n".join(lines))

render(600, 700, 1200, 1080, r"C:\Users\Luka\AppData\Local\Temp\opencode\chart_view.txt", scale=2, step=2)
render(600, 990, 1200, 1700, r"C:\Users\Luka\AppData\Local\Temp\opencode\chart_below.txt", scale=2, step=2)
print("done")