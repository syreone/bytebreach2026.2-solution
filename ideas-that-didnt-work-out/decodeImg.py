from PIL import Image
from pyzbar.pyzbar import decode

img = Image.open('gallery.png')
results = decode(img)
for r in results:
    print(repr(r.data))