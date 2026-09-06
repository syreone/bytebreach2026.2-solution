import zipfile, io

data = open('plate.png','rb').read()
i = data.rfind(b'PK\x03\x04')
print("zip offset:", i, "len:", len(data)-i)
buf = io.BytesIO(data[i:])
try:
    z = zipfile.ZipFile(buf)
    print("entries:", z.infolist())
    for e in z.infolist():
        print(e.filename, e.file_size, "encrypted:", (e.flag_bits & 1) == 1)
except Exception as ex:
    print("zipf open err:", ex)

# try extract with password
for pw in [b'q4v7nk2xr9tb6mhd', b'q4v7nk2xr9tb6mhd\n']:
    try:
        buf.seek(0)
        z = zipfile.ZipFile(buf)
        names = [e.filename for e in z.infolist()]
        for n in set(names+[names[0]]):
            try:
                d = z.read(n, pwd=pw)
                print("PASS!", pw, n, len(d))
                open(n+".dec",'wb').write(d)
            except RuntimeError as e:
                pass
        print("tried", pw)
    except Exception as ex:
        print("err", pw, ex)

# try common 'info-zip' style enc passwords
for pw in [b'R. Chalk', b'R.Chalk', b'mirabel', b'INHIBIT', b'MIRABEL', b'inhibit', b'panoplyvalley', b'panoply']:
    try:
        buf.seek(0)
        z = zipfile.ZipFile(buf)
        d = z.read(z.infolist()[0].filename, pwd=pw)
        print("PASS-ALT!", pw)
    except Exception:
        pass