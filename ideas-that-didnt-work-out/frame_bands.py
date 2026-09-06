import numpy as np, sys
from PIL import Image

im = np.array(Image.open("plate.png").convert("L")).astype(int)

def band(x0,y0,x1,y1,width,invert=False,name=None):
    crop = im[y0:y1, x0:x1]
    h, w = crop.shape
    height = max(1, int(round(h*width/w*0.5)))
    img = Image.fromarray(crop.astype(np.uint8)).resize((width, height))
    g = np.array(img).astype(float)
    if g.max() > g.min():
        g = (g-g.min())/(g.max()-g.min())
    else:
        g = np.zeros_like(g)
    if invert:
        g = 1-g
    cm = "@%#*+=-:. "
    rows = ["".join(cm[int(g[r,c]*(len(cm)-1))] for c in range(width)) for r in range(height)]
    name = name or "band"
    open(name+".txt","w").write("\n".join(rows))
    print(name, w, h)

# given picture bbox x186-1423 y294-942
band(0, 250, 1600, 320, 400, name="band_top_outer")       # light strip above picture (rows 250-320)
band(0, 280, 1600, 300, 400, name="band_top_inner")       # thin right at inner edge
band(0, 940, 1600, 1018, 400, name="band_bottom")         # below picture, full
band(0, 0, 190, 1018, 160, name="band_left")              # left border full height
band(1400, 0, 1600, 1018, 160, name="band_right")         # right border