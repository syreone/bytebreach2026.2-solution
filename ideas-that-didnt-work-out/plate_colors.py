import numpy as np
from PIL import Image

im = np.array(Image.open("plate.png").convert("RGB")).astype(int)
H, W, _ = im.shape
R = im[...,0]; G = im[...,1]; B = im[...,2]

# Inspect region colors: frame bbox x185-1575 y15-999
def stat(x0,y0,x1,y1,name):
    r=R[y0:y1,x0:x1]; g=G[y0:y1,x0:x1]; b=B[y0:y1,x0:x1]
    print(name, "R",r.mean(),r.min(),r.max(),"G",g.mean(),g.min(),g.max(),"B",b.mean(),b.min(),b.max())

stat(200,30,400,150,"top-left frame")
stat(400,30,1400,120,"top frame")
stat(200,60,1550,120,"frame band top rows60-120")
stat(200,900,1550,985,"frame band bottom rows900-985")
stat(200,120,1400,900,"interior rows120-900")
stat(0,0,1600,1018,"whole")
stat(100,60,200,900,"left frame col100-200")

# color histogram in frame band (rows 30-120, full width) - where ring top is
band = im[30:120, 100:1500].reshape(-1,3)
qs = np.quantile(band, [0.01,0.25,0.5,0.75,0.99], axis=0)
print("frame band quantiles:\n", qs)

# sample colors every 40 px along a horizontal line across the middle row of frame area (y=500)
row = 500
for x in range(0, W, 50):
    print(x, row, im[row, x].tolist(), "|gk?", (R[row,x]>170)&(G[row,x]>120)&(B[row,x]<140))