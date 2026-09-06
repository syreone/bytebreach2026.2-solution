from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.array(im)
r = a[:,:,0].astype(int); g = a[:,:,1].astype(int); b = a[:,:,2].astype(int)
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)

for x in range(1019, 1155):
    col = sat[:, x]
    idx = np.where(col > 60)[0]
    if len(idx):
        top = int(idx.min())
        bot = int(idx.max())
        h = bot - top
        sub = col[700:1000]
        ci = np.where(sub > 60)[0]
        mid = 700 + int(ci[len(ci)//2]) if len(ci) else int((top+bot)/2)
        print(x, "top=%4d bot=%4d h=%4d  c=(%d,%d,%d)" % (top, bot, h, int(r[mid,x]), int(g[mid,x]), int(b[mid,x])))