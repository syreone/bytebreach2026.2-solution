from PIL import Image

img = Image.open('gallery.png')
w, h = img.size

# bookshelf sits in the lower-middle area, on top of the teal credenza
cropped = img.crop((int(w*0.20), int(h*0.68), int(w*0.65), int(h*0.85)))
cropped = cropped.resize((cropped.width*2, cropped.height*2), Image.LANCZOS)
cropped.save('books_crop.png')
print("saved books_crop.png", cropped.size)
