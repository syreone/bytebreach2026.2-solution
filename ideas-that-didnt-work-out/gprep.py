from PIL import Image, ImageOps
import numpy as np

im = Image.open('gallery.png').convert('L')
crop = im.crop((0, 1500, 300, 1630))
for name, op in [('dark', lambda x: x), ('light', lambda x: ImageOps.invert(x))]:
    c = crop.resize((crop.size[0]*3, crop.size[1]*3), Image.LANCZOS)
    c = c.point(lambda p: 255 if p < 60 else 0)
    c.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\g_%s.png' % name) if name=='dark' else None
im2 = crop.point(lambda p: 255 if p < 90 else 0)
im2 = im2.resize((im2.size[0]*3, im2.size[1]*3), Image.LANCZOS)
im2.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\g_thr.png')
# also light-on-dark: threshold high
im3 = crop.point(lambda p: 255 if p > 190 else 0)
im3 = im3.resize((im3.size[0]*3, im3.size[1]*3), Image.LANCZOS)
im3.save(r'C:\Users\Luka\AppData\Local\Temp\opencode\g_hi.png')