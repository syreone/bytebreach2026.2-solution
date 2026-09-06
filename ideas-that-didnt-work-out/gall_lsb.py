import numpy as np
from PIL import Image

arr = np.array(Image.open('gallery.png').convert('RGB'))
H, W, C = arr.shape

def bits_of_byte(b):
    return [(b >> s) & 1 for s in range(8)]

def stream_lsb(arr, order=(0,1,2), lsb=True):
    bits = []
    for ch in order:
        for y in range(H):
            for x in range(W):
                bits.append((arr[y, x, ch] & 1) if lsb else ((arr[y, x, ch] >> 1) & 1))
    return bits

def to_bytes_reverse(bits):
    out = bytearray()
    for i in range(0, len(bits)//8*8, 8):
        b = 0
        for j in range(8):
            b |= bits[i+j] << (7-j)
        out.append(b)
    return bytes(out)

def score(data):
    return sum(1 for b in data if 32 <= b < 127 or b in (9,10,13)) / max(1, len(data))

bits = stream_lsb(arr, (0,1,2))
st = to_bytes_reverse(bits)
print("RGB lsb plain head:", st[:200])
print("score", score(st))
# find runs of printable
import re
for m in re.finditer(rb'[ -~]{4,}', st):
    print("run:", m.group(), "at", m.start())
# alpha-only score
alph = sum(1 for b in st if 65 <= b <= 90 or 97 <= b <= 122 or b == 32)
print("alpha score", alph/len(st))

# LSB plane images? just check top-left values
print("sample pixels", arr[0,0], arr[0,1], arr[1,0])