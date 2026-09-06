from PIL import Image
im = Image.open("gallery.png").convert("RGB")
im.crop((600, 600, 1200, 740)).resize((1200, 280), Image.LANCZOS).save(r"C:\Users\Luka\AppData\Local\Temp\opencode\crop_top.png")
im.crop((600, 996, 1200, 1600)).resize((1200, 1208), Image.LANCZOS).save(r"C:\Users\Luka\AppData\Local\Temp\opencode\crop_mid.png")
im.crop((600, 1200, 1200, 1620)).resize((1200, 840), Image.LANCZOS).save(r"C:\Users\Luka\AppData\Local\Temp\opencode\crop_mid2.png")
im.crop((0, 0, 618, 1000)).resize((618, 2000), Image.LANCZOS).save(r"C:\Users\Luka\AppData\Local\Temp\opencode\crop_left.png")
print("ok")