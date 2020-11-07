import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

fft_frame = 441
fname_path = glob.glob('test_bin/*')

for i, fname in enumerate(fname_path):
    base_name = fname.split('\\')[1]
    with open(fname, 'r') as f:
        num_data = np.array(f.readlines())
    num_data_f = fft(num_data)
    plt.plot(range(len(num_data_f)), np.abs(num_data_f))
    plt.xlim(0, 100)
    plt.savefig("test_image/" + str(i) + ".png")
    plt.close()