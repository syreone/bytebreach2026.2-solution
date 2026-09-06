import numpy as np
from PIL import Image

code = b"q4v7nk2xr9tb6mhd"
img = Image.open("plate.png").convert("RGB")
arr = np.array(img)
H, W, C = arr.shape

def bits_of(byte):
    return [(byte >> s) & 1 for s in range(8)]

def stream_lsb(arr, order=(2,1,0)):
    h, w, c = arr.shape
    bits = []
    for ch in order:
        for y in range(h):
            for x in range(w):
                bits.append(arr[y, x, ch] & 1)
    return bits

def to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits)//8*8, 8):
        b = 0
        for j in range(8):
            b |= bits[i+j] << (7-j)
        out.append(b)
    return bytes(out)

def score(data):
    printable = sum(1 for b in data if 32 <= b < 127 or b in (9,10,13))
    return printable / max(1, len(data))

def scan(stream, key, name):
    keystream = (key * (len(stream)//len(key) + 1))[:len(stream)]
    ks = np.frombuffer(keystream, dtype=np.uint8)
    st = np.frombuffer(stream, dtype=np.uint8)
    xor = st ^ ks
    # option A: read as-is
    a = to_bytes(list(xor))
    print("== %s XOR raw: score %.3f head %r" % (name, score(a), a[:120]))
    return a

# LSB stream by channel order RGB
for order in [(0,1,2),(1,0,2),(2,1,0),(0,2,1)]:
    bits = stream_lsb(arr, order)
    st = bytes((bits[i]) | (bits[i+1]<<1) | (bits[i+2]<<2) | (bits[i+3]<<3) |
               (bits[i+4]<<4) | (bits[i+5]<<5) | (bits[i+6]<<6) | (bits[i+7]<<7)
               for i in range(0, len(bits)//8*8, 8))
    scan(st, code, "order%s" % (order,))

# also try direct pixel-byte LSB (bit order reversed variant) and 7-bit
bits = stream_lsb(arr, (0,1,2))
st7 = bytes(sum(bits[i+j] << (6-j) for j in range(7)) if i+7 <= len(bits) else 0
            for i in range(0, len(bits)//7*7, 7))
scan(st7, code, "7bit")

# also just look for plaintext in the raw lsb stream without xor
st = bytes((bits[i]) | (bits[i+1]<<1) | (bits[i+2]<<2) | (bits[i+3]<<3) |
           (bits[i+4]<<4) | (bits[i+5]<<5) | (bits[i+6]<<6) | (bits[i+7]<<7)
           for i in range(0, len(bits)//8*8, 8))
print("plain lsb score", score(st), st[:80])