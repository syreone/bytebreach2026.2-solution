with open('plate.png', 'rb') as f:
    data = f.read()

iend = data.find(b'IEND')
trailing = data[iend+8:]

with open('hidden.zip', 'wb') as out:
    out.write(trailing)

print("wrote hidden.zip,", len(trailing), "bytes")
