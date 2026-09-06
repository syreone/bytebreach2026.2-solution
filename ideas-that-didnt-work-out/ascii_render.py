import numpy as np, sys
from PIL import Image

def ascii_render(arr, width=140, invert=False, charmap=None):
    if charmap is None:
        charmap = "@%#*+=-:. "
    im = Image.fromarray(arr).convert("L")
    w, h = im.size
    nh = max(1, int(round(h * width / w * 0.5)))
    im = im.resize((width, nh))
    g = np.array(im).astype(float)
    if g.max() > g.min():
        g = (g - g.min()) / (g.max() - g.min())
    else:
        g = np.zeros_like(g)
    g = 1 - g if invert else g
    idx = np.clip((g * len(charmap)).astype(int), 0, len(charmap)-1)
    rows = []
    for r in idx:
        rows.append("".join(charmap[i] for i in r))
    return "\n".join(rows)

if __name__ == "__main__":
    path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 140
    invert = len(sys.argv) > 3 and sys.argv[3] == "i"
    im = np.array(Image.open(path))
    print(ascii_render(im, width=width, invert=invert))