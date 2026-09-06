from PIL import Image

im = Image.open("gallery.png").convert("L")
crop = im.crop((560, 1050, 1175, 1200))
c = crop.resize((crop.width*3, crop.height*3), Image.LANCZOS)
c.save("glyph_strip.png")
print("saved", c.size)