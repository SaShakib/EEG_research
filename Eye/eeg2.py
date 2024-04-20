import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
# from pykalman import KalmanFilter
from scipy.signal import butter, filtfilt, detrend, find_peaks


# kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)



dat = pd.read_csv("../Live/eeg.csv")
data = dat[['id',	'ch1',	'ch2'	,'ch3',	'ch4', 'ch5']]
data = data.dropna()

# plt.figure(figsize=(60, 40))

# Initialize figure and axis
fig, ax = plt.subplots()

selected_channel = 'ch5'
eeg_data = data[selected_channel].values
time = data['id'].values

eeg_data = detrend(eeg_data)
cutoff_frequency = 10
sampling_rate = 256  
b, a = butter(N=4, Wn=cutoff_frequency / (0.5 * sampling_rate), btype='low')
eeg_data = filtfilt(b, a, eeg_data)


def exponential_moving_average(data, alpha=0.1):
    ema = [data[0]]  
    for i in range(1, len(data)):
        ema_value = alpha * data[i] + (1 - alpha) * ema[-1]
        ema.append(ema_value)
    return np.array(ema)



window_length_sec = 0.01
window_length_samples = int(window_length_sec * sampling_rate)

sma_smoothed_eeg = np.convolve(eeg_data, np.ones(window_length_samples) / window_length_samples, mode='same')
# kalman_smoothed_eeg, _ = kf.filter(sma_smoothed_eeg)
mean_value = np.mean(sma_smoothed_eeg)
sma_smoothed_eeg = sma_smoothed_eeg - mean_value


x_data = time[0:256]
y_data = data[selected_channel].values[0:256]
# line, = ax.plot(x_data, y_data, lw=1)

 

yxs_data = sma_smoothed_eeg[0:256]
l3, = ax.plot(x_data, yxs_data, lw=1)
# yx_data = kalman_smoothed_eeg[0:256]
# l2, = ax.plot(x_data, yx_data, lw=1)

first, secon = 1, 256

def update(frame):
    global first, secon

    x_data = (time[first:secon])
    # y_data = (data[selected_channel].values[first:secon])
    # yx_data = (smoothed_eeg[first:secon])
    yxs_data = (sma_smoothed_eeg[first:secon])
    # if len(x_data) > 100:
    #     x_data.pop(0)
    #     y_data.pop(0)
    first +=15
    secon +=15
    # line.set_data(x_data, y_data)
    # l2.set_data(x_data, yx_data)
    l3.set_data(x_data, yxs_data)
    ax.relim()
    ax.set_ylim((-1600,1600))
    ax.autoscale_view()
    return l3


ani = animation.FuncAnimation(fig, update, frames=None, interval=1)

# peaks, _ = find_peaks(-sma_smoothed_eeg, height=115)  # Adjust height threshold as needed

# Show plot
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

