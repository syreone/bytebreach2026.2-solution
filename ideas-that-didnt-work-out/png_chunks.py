import struct, zlib

def parse_png(path):
    data = open(path, "rb").read()
    print("file size:", len(data))
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8
    chunks = []
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos+4])[0]
        typ = data[pos+4:pos+8]
        body = data[pos+8:pos+8+ln]
        crc = data[pos+8+ln:pos+12+ln]
        chunks.append((typ, ln, body))
        pos += 12 + ln
        if typ == b"IEND":
            # trailing data after IEND
            trailing = data[pos:]
            print("IEND at pos", pos, "trailing bytes:", len(trailing))
            if trailing:
                print("trailing head:", trailing[:64])
        if pos >= len(data):
            break
    for typ, ln, body in chunks:
        if typ in (b"tEXt", b"zTXt", b"iTXt", b"tIME", b"eXIf"):
            print("chunk", typ, "len", ln, ":", body[:200])
    # also report IDAT count and size
    idat = sum(ln for t, ln, _ in chunks if t == b"IDAT")
    print("total IDAT:", idat)

parse_png("plate.png")