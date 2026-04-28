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

# Read and process signal
df = pd.read_excel('output.xlsx', usecols=['A'])
signal = df['A'].values
diff_sig = [signal[i+1] - signal[i] for i in range(len(signal)-1)]

dt = 0.050  # Sampling interval 50ms
fs = 1/dt   # Sampling frequency 20Hz
t = np.arange(0, len(diff_sig)*dt, dt) + dt

# Low-pass filter (cutoff frequency 2Hz)
cutoff_frequency = 2
filtered_sig = lowpass_filter(diff_sig, cutoff_frequency, fs)

plt.figure(figsize=(10, 6))
plt.plot(t, diff_sig, label='Original differential signal', alpha=0.5)
plt.plot(t, filtered_sig, label='Filtered signal', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Pressure change rate')
plt.legend()
plt.show()