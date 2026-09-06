from PIL import Image
import numpy as np

im = Image.open('chart_crop4.png').convert('L')
a = np.array(im).astype(float)
Hp, Wp = a.shape
Wc = 110
Hc = int(Wp/Hp*Wc*0.5)
small = Image.fromarray((((a<110)*255).astype(np.uint8))).resize((Wc, Hc), Image.LANCZOS)
g = np.array(small).astype(float)/255.0
cm = " .:-=+*#%@"
lines = ["".join(cm[min(int((1-g[r,c])*9.9),9)] for c in range(Wc)) for r in range(Hc)]
open(r'C:\Users\Luka\AppData\Local\Temp\opencode\crop4_ascii.txt','w').write("\n".join(lines))
print("ok", Wc, Hc)