from PIL import Image

img = Image.open('gallery.png')
# rough estimate — adjust based on result
cropped = img.crop((930, 960, 1190, 1610))
cropped.save('chart_crop.png')
print("saved chart_crop.png", cropped.size)
