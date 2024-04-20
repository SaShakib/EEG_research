import numpy as np
import matplotlib.pyplot as plt
import pylsl


# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_title('Streaming Data Plot')
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_xlim(0, 1)
ax.set_ylim(-1, 1)
plt.ion()  # Turn on interactive mode

# Create an empty buffer for storing data
x_buffer = []
y_buffer = []

# Initialize the LSL stream
stream_name = 'PetalStream_eeg'
print(f'Looking for a stream with name {stream_name}...')
streams = pylsl.resolve_streams('name', stream_name)
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {stream_name}')
inlet = pylsl.StreamInlet(streams[0])

# Main loop for updating the plot
while True:
    # Pull a sample from the LSL stream
    sample, timestamp = inlet.pull_sample()

    # Update the buffer with new data
    x_buffer.append(timestamp)
    y_buffer.append(sample)

    # Trim the buffer to keep only recent data
    buffer_length = len(x_buffer)
    if buffer_length > 1000:  # Limit buffer size to 1000 points
        x_buffer = x_buffer[buffer_length - 1000:]
        y_buffer = y_buffer[buffer_length - 1000:]

    # Update the plot with the new data
    line.set_xdata(x_buffer)
    line.set_ydata(y_buffer)
    ax.relim()
    ax.autoscale_view()

    # Update the plot
    plt.draw()
    plt.pause(0.003)  # Pause to allow time for the plot to update




'''
import numpy as np
import matplotlib.pyplot as plt
import pylsl


# Initialize the LSL stream
stream_name = 'PetalStream_eeg'
print(f'Looking for a stream with name {stream_name}...')
streams = pylsl.resolve_streams('name', stream_name)
if len(streams) == 0:
    raise RuntimeError(f'Found no LSL streams with name {stream_name}')
inlet = pylsl.StreamInlet(streams[0])

# Create a figure and axes for subplots
fig, axs = plt.subplots(4, 1, figsize=(8, 10))

# Main loop for updating the subplots
while True:
    # Pull a sample from the LSL stream
    sample, timestamp = inlet.pull_sample()

    # Plot each element of the sample array as a separate subplot
    for i in range(len(sample)):
        axs[i].clear()  # Clear the subplot
        axs[i].plot(sample[i])  # Plot the data
        axs[i].set_title(f'Subplot {i+1}')  # Set subplot title
        axs[i].set_xlabel('Time')
        axs[i].set_ylabel('Value')

    # Update the plot
    plt.tight_layout()  # Adjust subplot layout to prevent overlap
    plt.draw()
    plt.pause(0.003)  # Pause to allow time for the plot to update

'''