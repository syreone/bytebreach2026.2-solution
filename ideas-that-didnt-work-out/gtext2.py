from PIL import Image
import numpy as np

im = Image.open('gallery.png').convert('L')
# exact OCR boxes + margins
crop = im.crop((0, 1520, 240, 1620))
crop = crop.resize((crop.size[0]*4, crop.size[1]*4), Image.LANCZOS)
crop.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\gtext_big.png')
arr = np.array(im)
seg = arr[1520:1620, 0:240]
print("min", seg.min(), "max", seg.max(), "mean", round(seg.mean(),1))
# render ASCII 2-tone inverted: ink @
Wp, Hp = 240, 100
wide = 120
rows = int(wide*(Hp/Wp)*0.5)
small = Image.fromarray(((seg<128)*255).astype(np.uint8)).resize((wide, rows), Image.LANCZOS)
a = np.array(small).astype(float)/255.0
lines = ["".join("@" if a[r,c]>0.35 else " " for c in range(wide)) for r in range(rows)]
open(r'C:\Users\Luka\AppData\Local\Temp\opencode\gtext_2tone.txt','w').write("\n".join(lines))
print("ok")