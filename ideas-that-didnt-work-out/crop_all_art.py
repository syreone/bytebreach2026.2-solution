from PIL import Image

img = Image.open('gallery.png')
w, h = img.size

crops = {
    'mickey':  (0.13, 0.32, 0.34, 0.55),
    'canyon':  (0.62, 0.16, 0.95, 0.40),
    'pineapple': (0.35, 0.40, 0.50, 0.55),
    'collage': (0.52, 0.40, 0.75, 0.56),
}

for name, (x1, y1, x2, y2) in crops.items():
    c = img.crop((int(w*x1), int(h*y1), int(w*x2), int(h*y2)))
    c = c.resize((c.width*3, c.height*3), Image.LANCZOS)
    c.save(f'art_{name}.png')
    print(f'saved art_{name}.png')
