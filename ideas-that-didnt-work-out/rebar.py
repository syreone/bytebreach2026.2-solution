import numpy as np
from PIL import Image

arr = np.array(Image.open('chart_crop4.png').convert('RGB')).astype(float)
h, w, _ = arr.shape
palette = np.array([(255,192,192),(255,255,192),(192,255,192),
                    (192,255,255),(192,192,255),(255,192,255)])

d = np.sqrt(((arr[:,:,None,:] - palette[None,None,:,:])**2).sum(axis=3))
mind = d.min(axis=2)
which = d.argmin(axis=2)

segs = [(54,57),(66,69),(78,81),(90,93),(102,105),(114,117),(126,129),(138,141),(150,153),(162,165),(174,177)]
for (x1,x2) in segs:
    sub = mind[:, x1:x2+1].max(axis=1) < 60
    rows = np.where(sub)[0]
    print("bar %d..%d rows %d..%d len=%d color=%d" % (x1, x2, rows.min() if len(rows) else -1, rows.max() if len(rows) else -1, (rows.max()-rows.min()+1) if len(rows) else 0, which[len(rows)//2 if len(rows) else 0, (x1+x2)//2]))