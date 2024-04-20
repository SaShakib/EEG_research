import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
# from pykalman import KalmanFilter
from scipy.signal import butter, filtfilt, detrend, lfilter_zi, lfilter


# kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)


def butter_bandstop(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def apply_filter(data, lcut, hcut, fs, order, filter_type):
    if filter_type == 'bandstop':
        b, a = butter_bandstop(lcut, hcut, fs, order=order)
    elif filter_type == 'bandpass':
        b, a = butter_bandpass(lcut, hcut, fs, order=order)
    elif filter_type == 'highpass':
        b, a = butter_highpass(lcut, fs, order=order)
    zi = lfilter_zi(b, a)
    y, _ = lfilter(b, a, data, zi=zi*data[0])
    return y


dat = pd.read_csv("eeg.csv")
data = dat[['id',	'ch1',	'ch2'	,'ch3',	'ch4', 'ch5']]
data = data.dropna()

# plt.figure(figsize=(60, 40))

# Initialize figure and axis
fig, ax = plt.subplots()

selected_channel = 'ch4'
time = data['id']
data = data[selected_channel].values


# data = np.array(data)
        
        # Normalize data to have zero mean
data = data - np.mean(data)
        
        # Apply filters
data = apply_filter(data, 0.5, 256, 256, 5, 'highpass')
data = apply_filter(data, 30, 65, 256, 5, 'bandstop')
data = apply_filter(data, 103, 127, 256, 5, 'bandstop')
data = apply_filter(data, 1, 7, 256, 5, 'bandpass')

# eeg_data = detrend(eeg_data)
# cutoff_frequency = 15
# sampling_rate = 256  
# b, a = butter(N=4, Wn=cutoff_frequency / (0.5 * sampling_rate), btype='low')
# eeg_data = filtfilt(b, a, eeg_data)


# def exponential_moving_average(data, alpha=0.1):
#     ema = [data[0]]  
#     for i in range(1, len(data)):
#         ema_value = alpha * data[i] + (1 - alpha) * ema[-1]
#         ema.append(ema_value)
#     return np.array(ema)



# window_length_sec = 0.01
# window_length_samples = int(window_length_sec * sampling_rate)

# sma_smoothed_eeg = np.convolve(eeg_data, np.ones(window_length_samples) / window_length_samples, mode='same')
# # kalman_smoothed_eeg, _ = kf.filter(sma_smoothed_eeg)
# mean_value = np.mean(sma_smoothed_eeg)
# sma_smoothed_eeg = sma_smoothed_eeg - mean_value


x_data = time[0:256]
y_data = data[0:256]
line, = ax.plot(x_data, y_data, lw=1)

 

# yxs_data = sma_smoothed_eeg[0:256]
# l3, = ax.plot(x_data, yxs_data, lw=1)
# yx_data = kalman_smoothed_eeg[0:256]
# l2, = ax.plot(x_data, yx_data, lw=1)

first, secon = 1, 256

def update(frame):
    global first, secon

    x_data = (time[first:secon])
    y_data = (data[first:secon])
    # yx_data = (smoothed_eeg[first:secon])
    # yxs_data = (sma_smoothed_eeg[first:secon])
    # if len(x_data) > 100:
    #     x_data.pop(0)
    #     y_data.pop(0)
    first +=15
    secon +=15
    line.set_data(x_data, y_data)
    # l2.set_data(x_data, yx_data)
    # l3.set_data(x_data, yxs_data)
    ax.relim()
    ax.set_ylim((-1600,1600))
    ax.autoscale_view()
    return line


ani = animation.FuncAnimation(fig, update, frames=None, interval=1)

# peaks, _ = find_peaks(-sma_smoothed_eeg, height=115)  # Adjust height threshold as needed

# # Show plot
# plt.plot(time, sma_smoothed_eeg)
# plt.plot(time[peaks], sma_smoothed_eeg[peaks], 'ro')  # Mark detected peaks on the plot

plt.title('EEG signals')
plt.xlabel('Time (s)')
plt.ylabel('EGG channel data')
plt.grid(True)
plt.show()


# need to remove begining and ending boundary data, mayb tappering, or reflection 
# need to find negative peak and after one peak, no peak in 0.1 sec. and delta and theta will give spike. 
# https://medium.com/@daniel2023g/using-blinks-to-speak-759f0c0d46de make one script with this 
# then detect one with voltage 
# voltage and delta theta wave. 
# and one with paper 

