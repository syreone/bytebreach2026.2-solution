from PIL import Image
import numpy as np

im = Image.open("gallery.png").convert("RGB")
a = np.array(im)

# bars at x1019..1141, 12px pitch, 2px wide; tops ~745, baseline colored end y=996
bars = []
for i in range(11):
    xc = 1019 + i * 12  # center-ish? verify by scanning saturated columns below top
    col = a[:, xc]
    r, g, b = col[:, 0].astype(int), col[:, 1].astype(int), col[:, 2].astype(int)
    sat = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    colored = np.where(sat > 40)[0]
    top = colored.min()
    # find bottom: where colored region ends (last col both colored below 996)
    bottom = colored[colored < 1050].max()
    h = int(bottom) - int(top)
    bars.append((xc, int(top), int(bottom), h, r[colored.min()]))

print("letter by height//3:")
for xc, top, bottom, h, _ in bars:
    print(xc, "top=%d bottom=%d h=%3d  h/3=%3d  %s" % (top, bottom, h, h//3, chr(h//3)))