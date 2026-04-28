import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def lowpass_filter(data, cutoff_frequency, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# 读取并处理信号
df = pd.read_excel('output.xlsx', usecols=['A'])
signal = df['A'].values
diff_sig = [signal[i+1] - signal[i] for i in range(len(signal)-1)]

dt = 0.050  # 采样间隔50ms
fs = 1/dt   # 采样频率20Hz
t = np.arange(0, len(diff_sig)*dt, dt) + dt

# 低通滤波（截止频率2Hz）
cutoff_frequency = 2
filtered_sig = lowpass_filter(diff_sig, cutoff_frequency, fs)

plt.figure(figsize=(10, 6))
plt.plot(t, diff_sig, label='原始差分信号', alpha=0.5)
plt.plot(t, filtered_sig, label='滤波后信号', linewidth=2)
plt.xlabel('时间 (s)')
plt.ylabel('压力变化率')
plt.legend()
plt.show()