import wave, array

w = wave.open(r"C:\Users\Luka\cerberus-99-git\vault.wav", "rb")
sr = w.getframerate(); a = array.array("h", w.readframes(w.getnframes()))
ch = w.getnchannels()
mono = [a[i] for i in range(0, len(a), ch)]

strokes = [(1.00,2.60,"s1"),(3.10,4.17,"s2"),(4.75,6.25,"s3"),
           (6.77,8.23,"s4"),(8.54,10.08,"s5"),(10.50,12.02,"s6"),(12.46,13.96,"s7")]

for (t0,t1,nm) in strokes:
    s0=int(t0*sr); s1=int(t1*sr)
    seg=mono[s0:s1]
    peak=max(abs(x) for x in seg)
    rms=(sum(x*x for x in seg)/len(seg))**.5
    # dominant freq via zero crossings on 1s core
    z=0; prev=seg[0]>=0
    for x in seg[int(0.2*sr):int(0.8*sr)]:
        cur=x>=0
        if cur!=prev: z+=1
        prev=cur
    f=z/2/0.6
    print(nm, "peak%.0f rms%.0f"%(peak,rms), "fcross%.1f"%f)