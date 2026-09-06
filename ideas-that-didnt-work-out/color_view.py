from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.asarray(im).astype(int)

pal = {"R": np.array([255, 192, 192]), "Y": np.array([255, 255, 192]),
       "G": np.array([192, 255, 192]), "C": np.array([192, 255, 255]),
       "B": np.array([192, 192, 255]), "M": np.array([255, 192, 255])}

def cls(px):
    d = {k: np.abs(px - v).sum() for k, v in pal.items()}
    k = min(d, key=d.get)
    if d[k] < 90:
        return k
    r, g, b = px
    if r > 230 and g > 230 and b > 230:
        return " "
    if r < 60 and g < 60 and b < 60:
        return "#"
    return "."

def render(x0, y0, x1, y1, out, sx=2, sy=2):
    lines = []
    for y in range(y0, y1, sy):
        s = "".join(cls(a[y, x]) for x in range(x0, x1, sx))
        lines.append(s)
    with open(out, "w") as f:
        f.write("\n".join(lines))

render(1000, 700, 1150, 1010, r"C:\Users\Luka\AppData\Local\Temp\opencode\bars_color.txt", sx=1, sy=1)
render(600, 996, 1200, 1620, r"C:\Users\Luka\AppData\Local\Temp\opencode\below_bars.txt", sx=1, sy=1)
render(600, 600, 1000, 1010, r"C:\Users\Luka\AppData\Local\Temp\opencode\left_area.txt", sx=1, sy=1)
print("done")