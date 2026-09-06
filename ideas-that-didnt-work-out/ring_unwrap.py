import numpy as np
from PIL import Image
from scipy import ndimage

im = np.array(Image.open("plate.png").convert("RGB")).astype(int)
H, W, _ = im.shape
R = im[...,0]; G = im[...,1]; B = im[...,2]
gold = (R>170)&(G>120)&(B<140)

# clean small specks
gold2 = ndimage.binary_opening(gold, structure=np.ones((5,5)))
lab, n = ndimage.label(gold2)
print("components:", n)
sizes = ndimage.sum(gold2, lab, range(1, n+1))
big = sizes.argmax() + 1
ring = lab == big
print("ring pixels:", ring.sum(), "of gold", gold.sum())
filled = ndimage.binary_fill_holes(ring)
hole = filled & ~ring
print("hole pixels:", hole.sum())

# boundaries
inner_edge = ring & ndimage.binary_dilation(hole)
outer_edge = ring & ndimage.binary_dilation(~filled)  # ring pixels adjacent to outside

print("inner_edge px:", inner_edge.sum())
print("outer_edge px:", outer_edge.sum())

yy, xx = np.nonzero(filled)
cy, cx = float(yy.mean()), float(xx.mean())
print("filled center:", cx, cy)

# per-angle radius of inner edge and outer edge
n = 1440
angles = np.linspace(0, 2*np.pi, n, endpoint=False)
Y,X = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
DX = X - cx; DY = Y - cy
dist = np.hypot(DX, DY)
ang = (np.degrees(np.arctan2(DY, DX)) % 360) * (n/360.0)
aidx = ang.astype(int) % n

def edge_profile(mask):
    prof = np.full(n, np.nan)
    for i in range(n):
        m = aidx == i
        d = dist[mask & m]
        if d.size:
            prof[i] = np.median(d)
    return prof

r_i = edge_profile(inner_edge)
r_o = edge_profile(outer_edge)
valid = ~np.isnan(r_i) & ~np.isnan(r_o)
print("valid angles:", valid.sum())
# fill NaNs by interpolation
ri = np.interp(np.arange(n), np.where(valid)[0], r_i[valid])
ro = np.interp(np.arange(n), np.where(valid)[0], r_o[valid])
print("r_i min/mean/max:", ri.min(), ri.mean(), ri.max())
print("r_o min/mean/max:", ro.min(), ro.mean(), ro.max())
thick = ro - ri
print("thick min/mean/max:", thick.min(), thick.mean(), thick.max())

th = 120  # strip height
strip = np.zeros((n, th, 3), dtype=np.uint8)
for i in range(n):
    t = np.linspace(ro[i], ri[i], th)  # from outer to inner, top=outer
    px = cx + t*np.cos(angles[i])
    py = cy + t*np.sin(angles[i])
    for k in range(th):
        # bilinear sample
        x = px[k]; y = py[k]
        if 0 <= x < W-1 and 0 <= y < H-1:
            x0=int(x); y0=int(y); dx=x-x0; dy=y-y0
            I = im[y0:y0+2, x0:x0+2]
            v = (I[0,0]*(1-dx)*(1-dy) + I[0,1]*dx*(1-dy) +
                 I[1,0]*(1-dx)*dy + I[1,1]*dx*dy).astype(np.uint8)
            strip[i,k] = v

img = Image.fromarray(strip).transpose(Image.FLIP_TOP_BOTTOM)
img.save("ring_strip.png")
print("saved ring_strip.png", img.size)

g = img.convert("L")
gray = np.array(g).astype(int)
# dark = carved/ink
dark = gray < 90
print("dark fraction in strip:", dark.mean())
# print row means
rowavg = gray.mean(axis=1)
colavg = gray.mean(axis=0)
np.savez("ring_strip_meta.npz", rowavg=rowavg, colavg=colavg, ri=ri, ro=ro, n=n)
print("rowavg range:", rowavg.min(), rowavg.max())
print("colavg range:", colavg.min(), colavg.max())