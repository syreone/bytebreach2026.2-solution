import zipfile, struct

pwd = b"q4v7nk2xr9tb6mhd"

z = zipfile.ZipFile("plate.png")
print("=== ZIP listing ===")
for i in z.infolist():
    print(i.filename, "| size", i.file_size, "| csize", i.compress_size, "| method", i.compress_type,
          "| flag", hex(i.flag_bits), "| crc", hex(i.CRC), "| comment", i.comment, "| ext", i.extract_version, "| created", i.create_system)

print("\n=== gallery.png head (first 64 bytes) ===")
gd = z.read("gallery.png", pwd=pwd)
for i in range(0, min(64, len(gd)), 16):
    chunk = gd[i:i+16]
    hexs = " ".join("%02X" % b for b in chunk)
    asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print("%08X  %-48s  %s" % (i, hexs, asc))
print("gallery.png size:", len(gd))

# walk gallery.png PNG chunks
print("\n=== gallery.png chunk walk ===")
pos = 8
while pos < len(gd) - 8:
    ln, typ = struct.unpack(">I", gd[pos:pos+4]), gd[pos+4:pos+8]
    ln = ln[0]
    if typ not in (b"IDAT",):
        print("chunk @%d type=%s len=%d" % (pos, typ.decode("latin1"), ln))
    pos += 12 + ln
    if typ == b"IEND":
        break
print("end pos", pos, "remainder bytes:", len(gd) - pos)

# EOCD raw
eocd = data = open("plate.png", "rb").read()[-22:]
print("\n=== EOCD ===")
sig, n, d, cd, cds, cdl = struct.unpack("<IHHHHII", eocd[:18])
print("disk n=%d, cd entries=%d, cdsize=%d, cdoffset=%d, comment_len=%d" % (n, d, cd, cds, cdl))
print("comment:", eocd[18:])