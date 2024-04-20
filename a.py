import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to get CPU usage percentage
def get_cpu_percent():
    return psutil.cpu_percent()

# Initialize figure and axis
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=3)

# Function to update the plot
def update(frame):
    x_data.append(frame)
    y_data.append(get_cpu_percent())
    if len(x_data) > 100:
        x_data.pop(0)
        y_data.pop(0)
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    return line,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=None, interval=3.90625)

# Show plot
plt.title('CPU Usage Percentage')
plt.xlabel('Time (s)')
plt.ylabel('CPU Usage (%)')
plt.grid(True)
plt.show()
