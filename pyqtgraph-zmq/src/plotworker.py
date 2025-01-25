import random
import zmq
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class PlotWorker(QObject):
    data_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.running = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind("tcp://127.0.0.1:5555")
        self.counter = 0  # Initialize counter for x data
        self.y_buffer = []  # Buffer to store y data
        self.window_size = 100  # Define the window size for plotting

        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_data)
        self.timer.start(1000)  # Generate data every second

    def generate_data(self):
        if not self.running:
            return

        step_size = 1  # Define the step size for x data increment

        # Simulate spectroscopy data generation
        x = np.arange(self.counter, self.counter + self.window_size * step_size, step_size)  # Incrementing x data
        y = np.zeros_like(x, dtype=np.float64)  # Initialize y as a floating-point array

        # Add baseline noise
        baseline_noise = np.random.normal(0, 0.1, x.shape)  # Reduced baseline noise level
        y += baseline_noise

        # Add multiple peaks
        for _ in range(random.randint(1, 3)):  # Reduced number of peaks
            peak_position = random.uniform(x[0], x[-1])  # Peak position within the current window
            peak_height = random.uniform(1, 5)  # Reduced peak height in dB
            peak_width = random.uniform(1, 5)  # Reduced peak width in Hz
            peak_shape = random.choice(['gaussian', 'lorentzian'])

            if peak_shape == 'gaussian':
                y += peak_height * np.exp(-((x - peak_position) ** 2) / (2 * peak_width ** 2))
            elif peak_shape == 'lorentzian':
                y += peak_height / (1 + ((x - peak_position) / peak_width) ** 2)

        # Add some random noise
        noise = np.random.normal(0, 0.2, x.shape)  # Reduced noise level in dB
        y += noise

        # Ensure no zero values to avoid log10 issues
        y = np.clip(y, 1e-10, None)

        # Smooth transitions by adding a fraction of the previous y values
        if self.y_buffer:
            y = 0.5 * np.array(self.y_buffer[-self.window_size:]) + 0.5 * y

        # Append new y data to the buffer
        self.y_buffer.extend(y.tolist())

        # Keep only the most recent window_size data points
        if len(self.y_buffer) > self.window_size:
            self.y_buffer = self.y_buffer[-self.window_size:]

        # Send the current window of y values along with the corresponding x values
        self.socket.send_pyobj({'x': list(range(self.counter, self.counter + len(self.y_buffer))), 'y': self.y_buffer})

        self.counter += step_size  # Increment the counter for the next window

    def stop(self):
        self.running = False
        self.timer.stop()
        self.socket.close()
        self.context.term()