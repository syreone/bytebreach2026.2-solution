from PIL import Image
import numpy as np

arr = np.array(Image.open('gallery.png').convert('RGB')).astype(int)
# bar1 x 1015..1027, y 700..1010
def zoom(x0, x1, y0, y1, path, thr=60, wd=60):
    sub = arr[y0:y1, x0:x1]
    # find per-row min distance to bar1 color (255,192,192)
    pc = np.array([255,192,192])
    d = np.sqrt(((sub - pc[None,None,:])**2).sum(axis=2))
    # classify: close to bar color
    close = d < 80
    rows = np.where(close.sum(axis=1) > 0)[0]
    # render as text with . for bar-colored, @ for exact, o for background
    lines = []
    for r in range(0, close.shape[0]):
        rowd = d[r]
        row = close[r]
        s = ""
        for c in range(close.shape[1]):
            if rowd[c] < 25:
                s += "@"
            elif rowd[c] < 80:
                s += "+"
            elif rowd[c] < 150:
                s += "."
            else:
                s += " "
        lines.append("%4d %s" % (y0+r, s))
    open(path, 'w').write("\n".join(lines))
    print("wrote", path)

zoom(1015, 1027, 700, 1010, r'C:\Users\Luka\AppData\Local\Temp\opencode\bar1_zoom.txt')
zoom(1015, 1027, 700, 1010, r'C:\Users\Luka\AppData\Local\Temp\opencode\bar9_zoom.txt')
zoom(1015+84, 1015+96, 700, 1010, r'C:\Users\Luka\AppData\Local\Temp\opencode\bar9b_zoom.txt')  # bar9 x~1115