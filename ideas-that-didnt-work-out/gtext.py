from PIL import Image
import numpy as np

def render(path, box, wide, out, thr=150, inv=False):
    im = Image.open(path).convert('L')
    crop = im.crop(box)
    arrc = np.array(crop).astype(float)
    dark = arrc < thr
    # rows = wide * (h/w) * 0.5 (char aspect)
    Wp, Hp = box[2]-box[0], box[3]-box[1]
    rows = int(wide * (Hp/Wp) * 0.5)
    small = Image.fromarray((dark*255).astype(np.uint8)).resize((wide, rows), Image.LANCZOS)
    a = np.array(small).astype(float)/255.0
    cm = " .:-=+*#%@"
    lines = []
    for r in range(rows):
        line = ""
        for c in range(wide):
            v = a[r, c]
            if inv: v = 1-v
            line += cm[min(int((1-v)*9.99), 9)] if not inv else cm[min(int(v*9.99), 9)]
        lines.append(line)
    open(out, 'w').write("\n".join(lines))
    print("wrote", out)

render('gallery.png', (0, 1500, 600, 1700), 180, r'C:\Users\Luka\AppData\Local\Temp\opencode\gtext1.txt', thr=140)
render('gallery.png', (0, 1500, 250, 1700), 170, r'C:\Users\Luka\AppData\Local\Temp\opencode\gtext2.txt', thr=140)