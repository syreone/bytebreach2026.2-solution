import struct

data = open("plate.png", "rb").read()

# full EXIF decode
print("=== Full EXIF from plate.png tEXt at 60 ===")
exif_start = 60 + 8 + 4  # chunk @60 + 4 len + 4 type = 72
# actually let me re-walk chunks to find eXIf
pos = 8
while pos < len(data):
    ln = struct.unpack(">I", data[pos:pos+4])[0]
    typ = data[pos+4:pos+8]
    if typ == b"eXIf":
        payload = data[pos+8:pos+8+ln]
        print("EXIF payload (%d bytes):" % len(payload))
        print(payload.hex())
        # print readable strings
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in payload)
        print("ASCII:", asc)
        # try to find all text strings in EXIF
        i = 0
        while i < len(payload):
            if 32 <= payload[i] < 127:
                s = ""
                while i < len(payload) and 32 <= payload[i] < 127:
                    s += chr(payload[i])
                    i += 1
                if len(s) >= 3:
                    print("  string @%d: %r" % (i - len(s), s))
            else:
                i += 1
    pos += 12 + ln
    if typ == b"IEND":
        break

print("\n=== Searching ALL magic byte signatures in full plate.png ===")
magics = [
    (b"PK\x03\x04", "ZIP local"),
    (b"PK\x05\x06", "ZIP EOCD"),
    (b"PK\x07\x08", "ZIP data desc"),
    (b"\x7fELF", "ELF"),
    (b"MZ\x90\x00", "PE/EXE"),
    (b"MZP", "MZ/MZP"),
    (b"%PDF", "PDF"),
    (b"Rar!\x1a\x07", "RAR5"),
    (b"Rar!\x1a\x07\x00", "RAR4"),
    (b"7z\xbc\xaf\x27\x1c", "7Z"),
    (b"\xff\xd8\xff\xe0", "JPEG JFIF"),
    (b"\xff\xd8\xff\xe1", "JPEG EXIF"),
    (b"\xff\xd8\xff\xdb", "JPEG"),
    (b"GIF87a", "GIF87"),
    (b"GIF89a", "GIF89"),
    (b"BM", "BMP"),
    (b"RIFF", "RIFF"),
    (b"OggS", "OGG"),
    (b"fLaC", "FLAC"),
    (b"\x1aE\xdf\xa3", "MATROSKA"),
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"SQLite format 3", "SQLITE"),
    (b"\x04\x22\x4d\x18", "LZ4"),
    (b"\x28\xb5\x2f\xfd", "ZSTD"),
    (b"\x1f\x8b", "GZIP"),
    (b"BZh", "BZIP2"),
    (b"ID3", "MP3 ID3"),
    (b"\xff\xfb", "MP3"),
    (b"\xff\xf3", "MP3"),
    (b"\xff\xf2", "MP3"),
    (b"\x00\x00\x01\xb3", "MPEG video"),
    (b"\x00\x00\x01\xba", "MPEG-PS"),
    (b"\x49\x49\x2a\x00", "TIFF LE"),
    (b"\x4d\x4d\x00\x2a", "TIFF BE"),
    (b"PAR2", "PAR2"),
    (b"\x00PROI", "PROLOG"),
    (b"y!\xa5", "LZMA"),
    (b"\xfd7zXZ", "XZ"),
    (b"ustar", "TAR (at offset 257)"),
]
for m, label in magics:
    hits = []
    start = 0
    while True:
        i = data.find(m, start)
        if i < 0: break
        hits.append(i)
        start = i + 1
        if len(hits) > 20: break
    if hits:
        print("  %-20s %s  -> %s" % (label, m.hex(), [hex(h) for h in hits]))

print("\n=== Search for printable strings (>=6 chars) in plate.png raw binary ===")
i = 0
found = []
while i < len(data):
    if 32 <= data[i] < 127:
        s = ""
        while i < len(data) and 32 <= data[i] < 127:
            s += chr(data[i])
            i += 1
        if len(s) >= 6:
            found.append((i - len(s), s))
    else:
        i += 1
# print unique ones
for off, s in found:
    if not s.startswith("R. Chalk") and "IDAT" not in s:
        print("  @%d: %s" % (off, s))