with open('gallery.png', 'rb') as f:
    data = f.read()
iend = data.find(b'IEND')
print("IEND at:", iend, "/ total size:", len(data))
trailing = data[iend+8:]
print("trailing bytes:", len(trailing))
if trailing:
    print(trailing[:300])
