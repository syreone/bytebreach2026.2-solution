from PIL import Image

img = Image.open('gallery.png')
cropped = img.crop((965, 760, 1190, 1090))
cropped.save('chart_crop3.png')
print("saved chart_crop3.png", cropped.size)
