import numpy as np
from PIL import Image

im = Image.open('gallery.png').convert('L')
arr = np.array(im)
H, W = arr.shape
print("size", W, H)

# bottom 35%
crop = im.crop((0, int(H*0.65), W, H))
crop.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\gall_bottom.png')
wc = 140
hc = int(crop.size[1]/crop.size[0]*wc*0.45)
g = crop.resize((wc, hc), Image.LANCZOS)
a = np.array(g).astype(float)
a = (a-a.min())/(a.max()-a.min()+1e-9)
cm = " .:-=+*#%@"
lines = ["".join(cm[int(a[r,c]*9.99)] for c in range(wc)) for r in range(hc)]
open(r'C:\Users\Luka\AppData\Local\Temp\opencode\gall_bottom_ascii.txt','w').write("\n".join(lines))
print("bottom crop", crop.size, hc)