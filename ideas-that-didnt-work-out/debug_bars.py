from PIL import Image
import numpy as np

img = Image.open('chart_crop4.png').convert('RGB')
arr = np.array(img)
h, w, _ = arr.shape
print("image size:", w, h)

brightness = arr.sum(axis=2)
is_fg = brightness > 90

# save the foreground mask as a black/white image so we can SEE what's detected
mask_img = Image.fromarray((is_fg * 255).astype('uint8'))
mask_img.save('debug_mask.png')
print("saved debug_mask.png")

# also print per-column foreground pixel counts, every 5th column
for x in range(0, w, 5):
    count = is_fg[:, x].sum()
    print(f"x={x}: fg_pixel_count={count}")
