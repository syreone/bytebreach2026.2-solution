from PIL import Image

img = Image.open('gallery.png')
# more headroom on top (760 -> 700) and keep left/right/bottom similar
cropped = img.crop((965, 680, 1190, 1090))
cropped.save('chart_crop4.png')
print("saved chart_crop4.png", cropped.size)
