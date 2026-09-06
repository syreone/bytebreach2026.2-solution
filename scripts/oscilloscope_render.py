import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

rate, data = wavfile.read('vault.wav')
left = data[:, 0].astype(np.float64)
right = data[:, 1].astype(np.float64)

n = len(left)
parts = 3
size = n // parts

for i in range(parts):
    lo = i * size
    hi = n if i == parts - 1 else (i + 1) * size
    plt.figure(figsize=(10, 10), facecolor='black')
    plt.scatter(left[lo:hi], right[lo:hi], color='lime', s=0.15, alpha=0.6)
    plt.axis('off')
    plt.gca().set_facecolor('black')
    plt.gca().set_aspect('equal')
    plt.savefig(f'oscilloscope_part{i+1}.png', dpi=300, facecolor='black')
    print(f'saved oscilloscope_part{i+1}.png')