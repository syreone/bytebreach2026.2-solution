from PIL import Image

img = Image.open('plate.png')
print("size:", img.size)

# upscale the whole image 2x first so crops are easier to read
img2x = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
img2x.save('plate_2x.png')
print("saved plate_2x.png")
