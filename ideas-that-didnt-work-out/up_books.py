from PIL import Image

for src in ["books_crop.png"]:
    im = Image.open(src).convert("L")
    print(src, im.size)
    b = im.resize((im.width*3, im.height*3), Image.LANCZOS)
    b.save(r"C:\Users\Luka\cerberus-99-git\books_3x.png")