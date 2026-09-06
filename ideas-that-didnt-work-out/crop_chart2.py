from PIL import Image

img = Image.open('gallery.png')
# move up and narrow the vertical range to isolate just the black-framed chart
cropped = img.crop((930, 780, 1190, 1080))
cropped.save('chart_crop2.png')
print("saved chart_crop2.png", cropped.size)
