import sys
import numpy as np
from PIL import Image

def ocr_img(path_or_pil):
    pil = path_or_pil if isinstance(path_or_pil, Image.Image) else Image.open(path_or_pil)
    png = "ocr_tmp.png"
    pil.save(png)
    import asyncio, subprocess, os
    # use PowerShell WinRT OCR via a temp script
    script = r'''
param([string]$Path)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType=WindowsRuntime]
[Windows.Storage.StorageFile, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.RandomAccessStream, Windows.Foundation, ContentType=WindowsRuntime]
function Await($WinRtTask, $ResultType) {
    $asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
    $at = $asTask.MakeGenericMethod($ResultType).Invoke($null, @($WinRtTask))
    $at.Wait()
    $at.Result
}
[Windows.Storage.StorageFile]$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Path)) ([Windows.Storage.StorageFile])
$stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
foreach ($line in $result.Lines) { Write-Output $line.Text }
'''
    open("ocr_helper.ps1", "w").write(script)
    cp = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "ocr_helper.ps1", png], capture_output=True, text=True)
    return cp.stdout.strip()

from PIL import ImageOps, ImageFilter

pl = Image.open("plate.png").convert("L")
variants = {}
variants["normal"] = pl
variants["inverted"] = ImageOps.invert(pl)
variants["autocontrast"] = ImageOps.autocontrast(pl)
variants["equalize"] = ImageOps.equalize(pl)

for name, im in variants.items():
    for scale in (1, 2):
        s = im.resize((im.width*scale, im.height*scale), Image.LANCZOS)
        t = ocr_img(s)
        print("== %s x%d: %r" % (name, scale, t))