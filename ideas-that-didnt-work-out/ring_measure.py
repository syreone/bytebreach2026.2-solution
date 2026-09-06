import numpy as np
from PIL import Image

im = np.array(Image.open("plate.png").convert("RGB")).astype(int)
H, W, _ = im.shape
R = im[...,0]; G = im[...,1]; B = im[...,2]
gold = (R>170)&(G>120)&(B<140)

ys, xs = np.nonzero(gold)
cy, cx = float(ys.mean()), float(xs.mean())
print("center:", cx, cy)
print("count gold:", gold.sum())

# Measure radial profile around center
n = 1440
angles = np.linspace(0, 2*np.pi, n, endpoint=False)
r_in = np.zeros(n); r_out = np.zeros(n)
rmax = int(np.hypot(W, H))
yy = np.arange(H); xx = np.arange(W)
# For efficiency, precompute grid coords
Y,X = np.meshgrid(yy, xx, indexing='ij')
DX = X - cx; DY = Y - cy
dist = np.hypot(DX, DY)
ang = (np.degrees(np.arctan2(DY, DX)) % 360) * (n/360.0)

# Bin gold pixels into angle buckets, find min/max radius per bucket
idx = ang.astype(int) % n
r_bucket_min = np.full(n, 1e9)
r_bucket_max = np.full(n, -1e9)
count = np.zeros(n)
for p in range(0, gold.sum(), 1000000):
    pass

idx_g = idx[gold]; dist_g = dist[gold]
for i in range(n):
    m = idx_g == i
    if m.sum():
        r_bucket_min[i] = dist_g[m].min()
        r_bucket_max[i] = dist_g[m].max()
        count[i] = m.sum()

valid = count > 0
print("angles with gold:", valid.sum(), "of", n)
print("r_in min/mean/max:", r_bucket_min[valid].min(), r_bucket_min[valid].mean(), r_bucket_min[valid].max())
print("r_out min/mean/max:", r_bucket_max[valid].min(), r_bucket_max[valid].mean(), r_bucket_max[valid].max())
thick = r_bucket_max[valid] - r_bucket_min[valid]
print("thickness min/mean/max:", thick.min(), thick.mean(), thick.max())

np.savez("ring_geo.npz", angles=angles, r_in=r_bucket_min, r_out=r_bucket_max, cx=cx, cy=cy, n=n)