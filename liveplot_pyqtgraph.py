import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import pylsl


class StreamingPlot:
    def __init__(self, stream_name):
        # Initialize PyQtGraph application
        app = QtGui.QApplication(sys.argv)

        # Create a plot window
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('Streaming Data Plot')
        self.plt = self.win.addPlot(title='Streaming Data')
        self.curve = self.plt.plot()

        # Resolve the LSL stream
        print(f'Looking for a stream with name {stream_name}...')
        streams = pylsl.resolve_streams('name', stream_name)
        if len(streams) == 0:
            raise RuntimeError(f'Found no LSL streams with name {stream_name}')
        self.inlet = pylsl.StreamInlet(streams[0])

        # Start updating the plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(0)

        # Start the application event loop
        sys.exit(app.exec_())

    def update_plot(self):
        # Pull a sample from the LSL stream
        sample, timestamp = self.inlet.pull_sample()

        # Update the plot with the new data
        self.curve.setData(sample)


if __name__ == '__main__':
    stream_name = 'PetalStream_eeg'  # Specify the name of the LSL stream
    streaming_plot = StreamingPlot(stream_name)
