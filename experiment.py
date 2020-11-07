# -*- coding: utf-8 -*-

import sys
import wave
import math
import numpy as np
from scipy.io.wavfile import write
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt

wr = wave.open("sample3.wav", "r")

ch = wr.getnchannels()
fr = wr.getframerate()
fn = wr.getnframes()

data = wr.readframes(wr.getnframes())
num_data = np.frombuffer(data, dtype=np.int16)

if(wr.getnchannels() == 2):
    num_data = num_data[::2]
    
wr.close()

print_list = [524,595,647,648,705,706,759,760,827,828,883,961,962,1016,1017,1107,1108,1182,1183,1227,1228,1229,1230,1233,1234,1245,1246,1297,1298,1362,1363,1389,1390,1396,1420,1421,1487,1488,1538,1539,1577,1606,1607]

"""
for i in range(30000):
    num_data_f = fft(num_data[441*i:441*(i+1)])
    if i in print_list:
        num_data_f = np.abs(num_data_f)
        print(str(i) + ':' + str(np.argsort(-num_data_f[5:100])[0] + 5)
               + ':' + str(np.argsort(-num_data_f[5:100])[1] + 5)
                + ':' + str(np.argsort(-num_data_f[5:100])[2] + 5)
                + ':' + str(np.argsort(-num_data_f[5:100])[3] + 5)
                + ':' + str(np.argsort(-num_data_f[5:100])[4] + 5))


for i in range(25000,30000):
    num_data_f = fft(num_data[441*i:441*(i+1)])
    plt.plot(range(len(num_data_f)), np.abs(num_data_f))
    plt.xlim(0, 100)
    plt.ylim(0, 500000)
    plt.savefig("image/" + str(i) + ".png")
    plt.close()
"""

write('sample_fresco.wav', fr, num_data[3263400:3704400].astype(num_data.dtype))
# write('sample2_44100.wav', 44100, num_data.astype(num_data.dtype))
