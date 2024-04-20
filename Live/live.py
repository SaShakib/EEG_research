import argparse
import pylsl
from scipy.signal import butter, lfilter, lfilter_zi
import numpy as np
import time
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '192.168.0.100'
PORT = 80

# Connect to the ESP32
s.connect((HOST, PORT))


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

# fig, ax = plt.subplots()

# # Initialize a line object for the plot
# line, = ax.plot([], [])

# Function to update the plot


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--stream_name', type=str, required=True,
                    default='PetalStream_eeg', help='the name of the LSL stream')
args = parser.parse_args()

# first resolve an EEG stream
print(f'looking for a stream with name {args.stream_name}...')
streams = pylsl.resolve_stream('name', args.stream_name)

# create a new inlet to read from the stream
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {args.stream_name}')
inlet = pylsl.StreamInlet(streams[0])

rec = 3
startT = time.time()
endT = time.time()
countB = 0
buffer = []
fs = 256  # sampling frequency
buffer_size = 256  # buffer size set to 1 second of data
last_blink_time = None
refractory_period = 0.15  # in seconds
acCount = 0
active = False

left = 'L\n'
right = 'R\n'
moveF = 'S\n'
stopC = 'O\n'
lastInstruction = 'N'
leftorRight = True 

while True:
    sample, timestamp = inlet.pull_sample()
    buffer.append(sample[3])
    
    
         

    # If buffer is full, process the data and clear the buffer
    if len(buffer) >= buffer_size:

        if(countB == 1):
            startT = time.time()
            active = True
            print("Bit is active now \n")
            countB = 0
        
        if(active == True):
            endT = time.time()
            if(((endT - startT) > rec) and active):
                print(acCount)
                if(acCount == 0):
                    if(lastInstruction == 'N'):
                        lastInstruction = stopC
                        
                    s.sendall(lastInstruction.encode())
                elif(acCount == 1):
                    s.sendall(moveF.encode())
                    lastInstruction = 'N'
                    
                elif(acCount == 2):
                    s.sendall(left.encode())
                    lastInstruction = left
                else:                    
                    s.sendall(right.encode())
                    lastInstruction = right
                


                acCount = 0
                active = False
        
        data = np.array(buffer)
        
        # Normalize data to have zero mean
        data = data - np.mean(data)
        
        # Apply filters
        data = apply_filter(data, 0.5, fs, fs, 5, 'highpass')
        data = apply_filter(data, 57, 67, fs, 5, 'bandstop')
        data = apply_filter(data, 123, 127, fs, 5, 'bandstop')
        data = apply_filter(data, 1, 25, fs, 5, 'bandpass')
        
        # print(np.max(data))
        # Detect blink
        for i in range(2, len(data)):
            future = data[i]
            present = data[i - 1]
            past = data[i - 2]

            if (((present > past) and (present > future)) and present >= 140):
                current_time = time.time()
                if last_blink_time is None or (current_time - last_blink_time) > refractory_period:
                    print(data[i])
                    print("blink")
                    if(countB == 0 and active != True):
                        countB += 1
                    if(active):
                        acCount+=1
                    last_blink_time = current_time
            # if(np.max(data) >= 150):
            #     print("blink")

            # if (((present < past) and (present < future)) and present < -90):
            #     current_time = time.time()
            #     if last_blink_time is None or (current_time - last_blink_time) > refractory_period:
            #         print("blink")
            #         print(data[i])
            #         last_blink_time = current_time
        # ani = animation.FuncAnimation(fig, update, frames=range(buffer_size), fargs=[buffer, line],
                            # interval=1000.0/buffer_size, blit=True)
        # plt.show()

        # Keep the last two values of the buffer
        last_two_values = buffer[-2:]
        # Clear the buffer
        buffer = []
        # Prepend the last two values of the previous buffer to the new buffer
        buffer.extend(last_two_values)
