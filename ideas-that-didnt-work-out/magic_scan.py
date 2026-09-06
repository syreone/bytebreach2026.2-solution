import struct

data = open("plate.png", "rb").read()
print("file size:", len(data))

print("\n--- first 128 bytes hex ---")
for i in range(0, 128, 16):
    chunk = data[i:i+16]
    hexs = " ".join("%02X" % b for b in chunk)
    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print("%08X  %-48s  %s" % (i, hexs, asc))

# PNG chunks: walk the PNG structure until IEND to find where PNG actually ends
print("\n--- PNG chunk walk ---")
pos = 8
eight = struct.unpack(">I", data[:4])[0]
iend = None
while pos < len(data):
    ln, typ = data[pos:pos+4], data[pos+4:pos+8]
    ln = struct.unpack(">I", ln)[0]
    name = typ.decode("latin1")
    print("chunk @%d type=%s len=%d" % (pos, name, ln))
    pos += 12 + ln
    if name == "IEND":
        iend = pos
        break

print("PNG IEND end offset:", iend)

# find magic signatures anywhere
magics = [
    (b"PK\x03\x04", "ZIP local"),
    (b"PK\x05\x06", "ZIP EOCD"),
    (b"PK\x07\x08", "ZIP data desc"),
    (b"\x7fELF", "ELF"),
    (b"MZ", "PE/EXE"),
    (b"%PDF", "PDF"),
    (b"Rar!\x1a\x07", "RAR5"),
    (b"Rar!\x1a\x07\x00", "RAR"),
    (b"7z\xbc\xaf\x27\x1c", "7Z"),
    (b"\xff\xd8\xff", "JPEG"),
    (b"GIF8", "GIF"),
    (b"BM", "BMP"),
    (b"RIFF", "RIFF/WAV/AVI"),
    (b"OggS", "OGG"),
    (b"fLaC", "FLAC"),
    (b"\x1aE\xdf\xa3", "MATROSKA"),
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"SQLite format 3", "SQLITE"),
]
print("\n--- magic byte scan ---")
for m, label in magics:
    hits = []
    start = 0
    while True:
        i = data.find(m, start)
        if i < 0:
            break
        hits.append(i)
        start = i + 1
        if len(hits) > 40:
            break
    if hits:
        print("%-18s %s -> %s" % (label, m.hex(), hits[:12]))