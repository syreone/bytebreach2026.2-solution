from PIL import Image, ImageFilter, ImageOps

src = Image.open(r"C:\Users\Luka\cerberus-99-git\gallery.png").convert("L")
for k in (2, 3, 4):
    img = src.resize((src.width * k, src.height * k), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    img = ImageOps.autocontrast(img)
    out = r"C:\Users\Luka\cerberus-99-git\gallery_%dx.png" % k
    img.save(out)
    print(out, img.size)