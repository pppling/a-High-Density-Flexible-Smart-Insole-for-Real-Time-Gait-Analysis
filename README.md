# Smart Insole Design Based on Velostat

This project introduces a multifunctional Smart Insole system designed for real-time gait monitoring and plantar pressure analysis. By utilizing flexible Velostat piezoresistive material and IoT technologies, the system provides a low-cost yet high-density solution for sports performance and clinical rehabilitation.

## 1. Project Overview
The system captures foot pressure distribution through a 12x6 sensor matrix. Data is processed using advanced spatial clustering (DBSCAN) and temporal filtering to ensure high signal integrity for gait analysis.

### Key Features
* **Real-time Multi-point Monitoring**: High-density 72-point sensing matrix.
* **Robust Data Processing**: Spatial denoising via DBSCAN and temporal smoothing via Low-pass filtering.
* **Gait Analytics**: Automatic identification of foot contact states (forefoot, full-foot, heel) and step frequency calculation.
* **Dynamic Visualization**: Real-time heatmap rendering of pressure distribution.

## 2. System Architecture

### Hardware Components
* **Sensing Layer**: Velostat flexible piezoresistive film, conductive tape, and PET encapsulation.
* **Control Unit**: Arduino UNO/Lilypad integrated with CD74HC4067 multiplexers for array scanning.
* **Communication**: HC-05 Bluetooth module for wireless data transmission to PC.

### Software Workflow
1. **Data Acquisition (Arduino)**: Scans the 12x6 grid and sends voltage values (representing pressure) via Bluetooth.
2. **Online Processing (Python)**:
    * **Normalization**: Scales data for improved clustering performance.
    * **DBSCAN Clustering**: Denoises 3D data ($x, y$ coordinates and $z$ pressure values).
    * **Centroid Calculation**: Determines the pressure center to identify gait phases.
3. **Offline Analysis (Python)**:
    * **Low-pass Filtering**: Removes high-frequency noise from the signal sum.
    * **Frequency Processing**: Calculates step rate using forward difference and peak detection.

## 3. Software Modules

### Online: Real-time Collection & Visualization (`DBSCAN_final.py`)
* **Input**: Serial stream from Bluetooth.
* **Algorithm**: Uses KNN to estimate the `eps` parameter for DBSCAN.
* **Output**: A dynamic heatmap showing real-time foot pressure.

### Offline: Signal Filtering & Step Rate (`filter.py`)
* **Filtering**: Applies a Butterworth filter to the pressure sum.
* **Result**: For a typical walking test, the system calculated a frequency of **2.44 Hz**, equivalent to **146 steps per minute**.

## 4. Experimental Results
* **Dynamic Heatmap**: Successfully visualizes the transition from heel-strike to toe-off.
* **Accuracy**: The dual-filtering approach (DBSCAN + Low-pass) significantly reduces sensor artifacts caused by the "creep" effect of Velostat.

