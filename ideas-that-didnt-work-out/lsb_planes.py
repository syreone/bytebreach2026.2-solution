from PIL import Image
import numpy as np

img = Image.open('plate.png')
print("mode:", img.mode, "size:", img.size)
arr = np.array(img)

channels = arr.shape[2] if arr.ndim == 3 else 1
for ch in range(channels):
    plane = (arr[..., ch] & 1) * 255
    Image.fromarray(plane.astype('uint8')).save(f'plate_lsb_channel{ch}.png')
    print(f'saved plate_lsb_channel{ch}.png')
