import struct

data = open("plate.png", "rb").read()
pos = 8
body = None
while pos < len(data):
    ln = struct.unpack(">I", data[pos:pos+4])[0]
    typ = data[pos+4:pos+8]
    b = data[pos+8:pos+8+ln]
    if typ == b"eXIf":
        body = b
        break
    pos += 12 + ln

print("exif len:", len(body))
print(body.hex())
print()
# try printing the tail after 'ASCII'
idx = body.find(b"ASCII")
print("ASCII tag at", idx)
print("tail:", body[idx:])