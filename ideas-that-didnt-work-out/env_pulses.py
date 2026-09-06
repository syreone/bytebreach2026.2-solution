import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
raw = a = array.array("h", w.readframes(n))
mono = [a[i] for i in range(0, len(a), ch)]

# envelope over 15s at ~ (44.1k/ ~ 1k) resolution
win = 120  # ~2.7ms
env = []
for i in range(0, int(15.0*sr), win):
    chunk = mono[i:i+win]
    env.append(max(abs(j) for j in chunk))

mx = max(env)
thresh = 0.5 * mx
# segment into on/off runs, compress: durations in ms
runs = []
cur = env[0] >= thresh
count = 0
for e in env:
    b = e >= thresh
    if b == cur:
        count += 1
    else:
        runs.append((cur, count * win / 1000))
        cur = b; count = 1
runs.append((cur, count * win / 1000))

print("max env", mx)
# print runs as sequence of short/long
chars = []
for on, d in runs:
    if d < 5:  continue
    if on: chars.append(("#" if d < 260 else "="))
    else:  chars.append(("-" if d < 260 else "_"))
print("".join(chars))
for r in runs:
    print("%s %.0fms" % ("ON " if r[0] else "OFF", r[1]))