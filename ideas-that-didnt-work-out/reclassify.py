from PIL import Image
import colorsys

im = Image.open("gallery.png").convert("RGB")
xs = list(range(1019, 1142, 12))
# bar vertical extent ~996..1370 (shorter bar 195px => top 1370? no: ytop = 1565-h? measure again later)
# collect all pixels in the bar column x..x+4, y 900..1400; compute max saturation
def maxsat(x):
    best = None
    for y in range(900, 1500, 2):
        for dx in (0,1):
            r,g,b = im.getpixel((x+dx, y))
            h,l,s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            if best is None or s > best[0]:
                best = (s, h, l, (r,g,b), y)
    return best

for i, x in enumerate(xs):
    (s,h,l,rgb,y) = maxsat(x)
    deg = int(h*360) % 360
    # classify
    if s < 0.15:
        name = "GRAY(.%02d)" % int(s*100)
    elif l < 0.2:
        name = "DARK"
    elif deg < 15: name = "RED"
    elif deg < 45: name = "ORANGE"
    elif deg < 70: name = "YELLOW"
    elif deg < 160: name = "GREEN"
    elif deg < 200: name = "CYAN"
    elif deg < 260: name = "BLUE"
    elif deg < 300: name = "MAGENTA"
    else: name = "RED/PINK"
    print("b%-2d sat=%.2f hue=%3d l=%.2f %s at y%d" % (i+1, s, deg, l, name, y), rgb)