import struct, zlib

def dump_png_chunks(fn, name=""):
    data = open(fn, "rb").read()
    pos = 8
    print("=== %s (%d bytes) ===" % (name or fn, len(data)))
    while pos < len(data) - 8:
        ln = struct.unpack(">I", data[pos:pos+4])[0]
        typ = data[pos+4:pos+8]
        payload = data[pos+8:pos+8+ln]
        if typ not in (b"IDAT",):
            print("  chunk @%d type=%s len=%d  payload=%r" % (pos, typ.decode("latin1"), ln, payload[:200]))
        pos += 12 + ln
        if typ == b"IEND":
            break
    print("ends at %d / %d" % (pos, len(data)))
    print()

dump_png_chunks("plate.png", "plate.png")
dump_png_chunks("gallery.png", "gallery.png")

print("=== also list all .png in current dir with tEXt/iTXt/other ===")
import glob, os
for fn in glob.glob("*.png"):
    base = os.path.basename(fn)
    data = open(fn, "rb").read()
    if len(data) < 60:
        continue
    found = []
    pos = 8
    while pos < len(data) - 8:
        ln = struct.unpack(">I", data[pos:pos+4])[0]
        typ = data[pos+4:pos+8]
        payload = data[pos+8:pos+8+ln]
        if typ in (b"tEXt", b"iTXt", b"zTXt", b"eXIf", b"pHYs", b"tIME", b"gAMA"):
            found.append("%s@%d=(%r)" % (typ.decode("latin1"), pos, payload[:80]))
        pos += 12 + ln
        if typ == b"IEND":
            break
    if found:
        print(fn, "->", found)