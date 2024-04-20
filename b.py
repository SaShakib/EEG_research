import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize empty lists for storing data
x_data = []
y_data = [[] for _ in range(4)]  # Initialize empty lists for 4 subplots

# Initialize counter and time interval
timestamp_counter = 0
time_interval = 0.1  # Interval in seconds

# Function to generate random data
def get_data():
    # Generate random sample data for each subplot
    sample = np.random.randint(1, 401, size=4)
    return sample

# Initialize figure and axes for subplots
fig, axs = plt.subplots(4, 1, figsize=(8, 10))
lines = [ax.plot([], [], lw=3)[0] for ax in axs]

# Function to update the plot
def update(frame):
    global timestamp_counter
    # Increment timestamp counter by time interval
    timestamp_counter += time_interval
    # Get data
    timestamp = timestamp_counter
    sample = get_data()
    # Append data to buffers
    x_data.append(timestamp)
    for i in range(4):
        y_data[i].append(sample[i])
        # Trim the buffer to keep only the most recent 100 data points
        if len(x_data) > 50:
            x_data.pop(0)
        if len(y_data[i]) > 50:
            y_data[i].pop(0)
        # Update the line data for each subplot
        lines[i].set_data(x_data, y_data[i])
        axs[i].relim()
        axs[i].autoscale_view()
    return lines

# Create animation
ani = animation.FuncAnimation(fig, update, frames=None, interval=3)

# Show plot
plt.show()
