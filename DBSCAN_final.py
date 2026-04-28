import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from matplotlib.animation import FuncAnimation
from pylab import mpl
import pandas as pd
import serial
import time
import re

# 计算eps参数
def estimate_eps(data, k=5):
    neighbors = NearestNeighbors(n_neighbors=k)
    neighbors_fit = neighbors.fit(data)
    distances, _ = neighbors_fit.kneighbors(data)
    return np.mean(distances[:, k-1])

# 计算压力质心
def calculate_centroid(points):
    weights = points[:, 2]
    sum_weighted_x = np.sum(points[:, 0] * weights)
    sum_weighted_y = np.sum(points[:, 1] * weights)
    sum_weights = np.sum(weights)
    if sum_weights == 0: return np.array([0, 0])
    return np.array([sum_weighted_x / sum_weights, sum_weighted_y / sum_weights])

def update(frame):
    global t, signal_t, ser, idx, z_values, z_0, flag
    while True:
        data = ser.readline()
        mydata = re.sub('\r|\n','',data.decode())
        if mydata == "a":
            idx = 0
        elif mydata == "b":
            break
        else:
            val = int(mydata)
            if abs(val - z_values[idx%12 * 6 + idx//12]) > 15:
                z_values[idx%12 * 6 + idx//12] = val
            idx += 1
    
    if flag > 0:
        z_0 = z_values
        flag -= 1
    current_z = z_values - z_0
    
    points = np.vstack((xx, yy, current_z)).T
    center = calculate_centroid(points)
    
    # 状态识别
    jiaozhang = '全脚掌'
    if center[1] > 14: jiaozhang = '后脚掌'
    elif center[1] < 8: jiaozhang = '前脚掌'
    
    # DBSCAN聚类去噪
    scaler = StandardScaler()
    points_normalized = scaler.fit_transform(points)
    dbscan = DBSCAN(eps=estimate_eps(points_normalized), min_samples=6)
    labels = dbscan.fit_predict(points_normalized)
    
    # 计算有效信号总和
    signal_sum = sum(current_z[i] for i, label in enumerate(labels) if label != -1)
    signal_t.append(signal_sum)
    
    z_matrix = np.array(current_z).reshape(12, 6)
    heatmap.set_data(z_matrix)
    ax.set_title(f'Frame={frame}, Center={center}, State={jiaozhang}')
    return heatmap,

if __name__ == "__main__":
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    ser = serial.Serial('COM11', 38400)
    z_values, z_0, flag = np.zeros(72), np.zeros(72), 2
    x_spacing, y_spacing = 1.5, 2.0
    x_coords = np.arange(0, 6 * x_spacing, x_spacing)
    y_coords = np.arange(0, 12 * y_spacing, y_spacing)
    xx, yy = np.meshgrid(x_coords, y_coords)
    xx, yy = xx.flatten(), yy.flatten()
    
    fig, ax = plt.subplots(figsize=(8, 10))
    heatmap = ax.imshow(np.zeros((12, 6)), cmap='hot_r')
    ani = FuncAnimation(fig, update, frames=100, interval=50, blit=False)
    plt.show()
    
    pd.DataFrame(signal_t, columns=['A']).to_excel('output.xlsx', index=False)