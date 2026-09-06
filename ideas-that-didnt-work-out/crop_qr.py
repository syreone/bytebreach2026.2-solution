from PIL import Image

img = Image.open('gallery.png')
w, h = img.size

# QR code is top-left area of the gallery wall
cropped = img.crop((int(w*0.14), int(h*0.10), int(w*0.38), int(h*0.28)))
cropped = cropped.resize((cropped.width*3, cropped.height*3), Image.NEAREST)
cropped.save('qr_crop.png')
print("saved qr_crop.png", cropped.size)
