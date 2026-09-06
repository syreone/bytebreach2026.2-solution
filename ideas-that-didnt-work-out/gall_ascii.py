import numpy as np
from PIL import Image

im = Image.open('gallery.png').convert('L')
W = 120
ar = im.size[1]/im.size[0]
H = int(W*ar*0.5)
g = im.resize((W, H), Image.LANCZOS)
a = np.array(g).astype(float)
a = (a-a.min())/(a.max()-a.min()+1e-9)
cm = " .:-=+*#%@"
lines = ["".join(cm[int(a[r,c]*9.99)] for c in range(W)) for r in range(H)]
open(r'C:\Users\Luka\AppData\Local\Temp\opencode\gallery_ascii.txt','w').write("\n".join(lines))
print("done", W, H)