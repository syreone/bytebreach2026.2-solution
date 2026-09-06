import numpy as np
from PIL import Image

im = Image.open('gallery.png').convert('RGB')
arr = np.array(im)
H, W, C = arr.shape
print("shape", arr.shape)

# find the bar chart area: rows where many non-background pixels
# detect unique colors to understand the scene
cols, counts = np.unique(arr.reshape(-1,3), axis=0, return_counts=True)
order = np.argsort(-counts)
print("top colors:")
for i in order[:12]:
    print(cols[i], counts[i], "%.3f%%" % (100*counts[i]/(H*W)))

# OCR the whole image
import subprocess, json
script = r'''
Add-Type -AssemblyName System.Runtime.WindowsRuntime;
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime];
$null = [Windows.Foundation.IAsyncOperation``1, Windows.Foundation, ContentType=WindowsRuntime];
$file = [Windows.Storage.StorageFile]::GetFileFromPathAsync("C:\Users\Luka\cerberus-99-git\gallery.png").GetAwaiter().GetResult();
$stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult();
$dec = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult();
$bmp = $dec.GetSoftwareBitmapAsync().GetAwaiter().GetResult();
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages();
$rslt = $engine.RecognizeAsync($bmp).GetAwaiter().GetResult();
$rslt.Text
'''
open(r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_all.ps1','w').write(script)
r = subprocess.run(['powershell','-ExecutionPolicy','Bypass','-File',r'C:\Users\Luka\AppData\Local\Temp\opencode\ocr_all.ps1'], capture_output=True, text=True)
print("OCR:", r.stdout, r.stderr)