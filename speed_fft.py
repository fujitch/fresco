# -*- coding: utf-8 -*-

import sys
import wave
import numpy as np
from scipy.fftpack import fft, ifft

if len(sys.argv) == 1:
    sys.exit()

distance = 0.007

# 打球音を受け付けない0.15秒は時速168km
reset_criteria = 0.15

wr = wave.open(sys.argv[1], "r")

ch = wr.getnchannels()
fr = wr.getframerate()
fn = wr.getnframes()

data = wr.readframes(wr.getnframes())
num_data = np.frombuffer(data, dtype=np.int16)

if(wr.getnchannels() == 2):
    num_data = num_data[::2]
    
wr.close()

fft_frame = int(fr / 100)

def is_hit_frame(data):
    data_abs = np.abs(data)[:int(fft_frame / 4)]
    if np.argmax(data_abs[5:]) == 4 or np.argmax(data_abs[5:]) == 5 or np.argmax(data_abs[5:]) == 6:
        if np.max(data_abs[9:12]) / np.sum(data_abs[5:]) > 0.1:
        #if np.max(data_abs[5:]) > 200000:
            return True
    return False

pre_hit_frame = 0

a = []
for i in range(0, len(num_data), int(fft_frame / 2)):
    num_data_f = fft(num_data[i:i+fft_frame])
    if is_hit_frame(num_data_f):
        if pre_hit_frame != 0:
            duration_frame = i - pre_hit_frame
            if duration_frame > fr * reset_criteria:
                print('speed: ' + str(distance * 3600 * fr / duration_frame) + ', frame: ' + str(i / 441) + ', arg: ' + str(np.argmax(np.abs(num_data_f)[:int(fft_frame / 4)][5:])))
                pre_hit_frame = i
        else:
            pre_hit_frame = i