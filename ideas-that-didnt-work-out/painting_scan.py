import numpy as np
from PIL import Image

p = "C:/Users/Luka/AppData/Local/Temp/opencode/painting.jpg"
im = np.array(Image.open(p).convert("RGB")).astype(int)
H, W, _ = im.shape
print("size", W, H)
g = im.mean(axis=2)
# text = dark strokes on light
dark = g < 100
print("dark frac:", dark.mean())
# column & row profiles of the dark mask
rowprof = dark.mean(axis=1)
colprof = dark.mean(axis=0)
# ASCII two-level overview at 120 cols
cm = ".%"
import sys
sys.path.insert(0, ".")
from ascii_render import ascii_render
print(ascii_render(im.astype(np.uint8), width=120))