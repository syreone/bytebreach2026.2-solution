from PIL import Image

img = Image.open('gallery.png')
w, h = img.size
print("size:", w, h)

# rough estimate - vertical strip between hallway photo and black chart frame
cropped = img.crop((int(w*0.66), int(h*0.48), int(w*0.78), int(h*0.70)))
cropped = cropped.resize((cropped.width*3, cropped.height*3), Image.LANCZOS)
cropped.save('ornaments_crop.png')
print("saved ornaments_crop.png", cropped.size)
