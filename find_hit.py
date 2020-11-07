
import sys
import math
import numpy as np
from scipy.fftpack import fft, ifft

rms_count = 0
for_rms_frames = []
fft_frame = 441
pre_data = np.zeros((fft_frame))
rms_criteria = 5.0

def rms(data):
    mean = sum(data)/len(data)
    data = data - mean
    data = np.power(data,2)
    rms = math.sqrt(sum(data)/len(data))
    return rms

while True:
    stdin = input()
    if stdin == 'complete':
        break
    else:
        try:
            with open(stdin, 'r') as f:
                num_data = np.array(f.readlines())
                # 開始30framesで環境音を採取する
                if rms_count < 30:
                    num_data_f = fft(num_data)
                    data_abs = np.abs(num_data_f)[:int(fft_frame / 4)]
                    for d in data_abs:
                        for_rms_frames.append(d)
                    rms_count += 1
                elif rms_count == 30:
                    rms_criteria = rms(for_rms_frames) * 7
                    rms_count += 1
                # 前のframeと重複して判定
                num_data_pre = np.zeros((fft_frame))
                num_data_pre[:220] = pre_data[221:]
                num_data_pre[220:] = num_data[:221]
                num_data_pre_f = fft(num_data_pre)
                data_abs_pre = np.abs(num_data_pre_f)[:int(fft_frame / 4)]
                if np.argmax(data_abs_pre[5:]) == 4 or np.argmax(data_abs_pre[5:]) == 5 or np.argmax(data_abs_pre[5:]) == 6:
                    if np.max(data_abs_pre[5:]) > rms_criteria:
                    #if np.max(data_abs_pre[9:12]) / np.sum(data_abs_pre[5:]) > 0.1:
                        print(stdin.strip()+'OK')
                        sys.stdout.flush()
                        pre_data = num_data
                        continue
                num_data_f = fft(num_data)
                data_abs = np.abs(num_data_f)[:int(fft_frame / 4)]
                if np.argmax(data_abs[5:]) == 4 or np.argmax(data_abs[5:]) == 5 or np.argmax(data_abs[5:]) == 6:
                    # if np.max(data_abs[9:12]) / np.sum(data_abs[5:]) > 0.1:
                    if np.max(data_abs[5:]) > rms_criteria:
                        print(stdin.strip()+'OK')
                        sys.stdout.flush()
                pre_data = num_data
        except:
            print(stdin.strip())
            sys.stdout.flush()
        print(stdin.strip())
        sys.stdout.flush()
        