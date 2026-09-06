import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage as ndi

im = np.array(Image.open("plate.png").convert("RGB")).astype(float)
R = im[...,0]; G = im[...,1]; B = im[...,2]

# cold light = blue channel; varnish flares in warm. Compute "blue minus red"
c = B - R
s = np.percentile(c, 2), np.percentile(c, 98)
norm = ((c - s[0])/(s[1]-s[0])*255).astype(np.uint8)
Image.fromarray(norm).save("plate_blue_minus_red.png")

# also blue channel alone equalized
be = ImageOps.equalize(Image.fromarray(B.astype(np.uint8)))
be.save("plate_blue_equal.png")

# high-pass of blue channel
blur = ndi.gaussian_filter(B, 8)
hp = B - blur
s2 = np.percentile(hp, 3), np.percentile(hp, 97)
hpn = ((hp - s2[0])/(s2[1]-s2[0])*255).astype(np.uint8)
Image.fromarray(hpn).save("plate_blue_hp.png")

# quick ASCII of the blue-minus-red overview
import sys
sys.path.insert(0, ".")
from ascii_render import ascii_render
print("=== blue-minus-red ===")
print(ascii_render(norm, width=140))
print()
print("=== blue high-pass ===")
print(ascii_render(hpn, width=140))