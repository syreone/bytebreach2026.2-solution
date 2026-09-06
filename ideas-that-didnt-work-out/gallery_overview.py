import numpy as np
from PIL import Image
import sys
sys.path.insert(0, ".")
from ascii_render import ascii_render

g = np.array(Image.open("gallery.png").convert("L")).astype(int)
h, w = g.shape
print("gallery size", w, h)
print(ascii_render(g.astype(np.uint8), width=120))