with open('plate.png', 'rb') as f:
    data = f.read()

iend = data.find(b'IEND')
print("IEND found at byte:", iend)
print("Total file size:", len(data))
trailing = data[iend+8:]  # skip IEND + 4-byte CRC
print("Bytes after IEND:", len(trailing))
if trailing:
    print(trailing[:500])
