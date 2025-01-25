from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, mkPen
import sys
import zmq
import numpy as np
from plotworker import PlotWorker
from threading import Thread
from pyqtgraph import InfiniteLine, TextItem

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Plotting App via ZeroMQ")
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.plot_data = {'x': [], 'y': []}
        self.plot_curve = self.plot_widget.plot(pen=mkPen('r', width=2))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect("tcp://127.0.0.1:5555")

        self.worker = PlotWorker()
        self.worker_thread = Thread(target=self.worker.generate_data)
        self.worker_thread.start()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update plot every second

        self.init_ui()

        # Add hover lines and label
        self.vline = InfiniteLine(angle=90, movable=False, pen=mkPen('g', width=1))
        self.hline = InfiniteLine(angle=0, movable=False, pen=mkPen('g', width=1))
        self.plot_widget.addItem(self.vline, ignoreBounds=True)
        self.plot_widget.addItem(self.hline, ignoreBounds=True)
        self.label = TextItem("", anchor=(0, 1), color='w')
        self.plot_widget.addItem(self.label)
        self.plot_widget.scene().sigMouseMoved.connect(self.on_mouse_move)

        self.plot_widget.setLabel('left', 'Magnitude', units='dB')
        self.plot_widget.setLabel('bottom', 'Frequency')

    def init_ui(self):
        toolbar = self.addToolBar("Control")
        stop_button = QtWidgets.QPushButton("Stop")
        stop_button.clicked.connect(self.stop_plotting)
        toolbar.addWidget(stop_button)

        resume_button = QtWidgets.QPushButton("Resume")
        resume_button.clicked.connect(self.resume_plotting)
        toolbar.addWidget(resume_button)

    def update_plot(self):
        try:
            while True:
                data = self.socket.recv_pyobj(flags=zmq.NOBLOCK)
                self.plot_data['x'] = data['x']
                self.plot_data['y'] = data['y']
                self.plot_curve.setData(self.plot_data['x'], self.plot_data['y'])
                self.plot_widget.autoRange()  # Automatically rescale the axes
        except zmq.Again:
            pass

    def stop_plotting(self):
        self.timer.stop()

    def resume_plotting(self):
        self.timer.start(1000)

    def closeEvent(self, event):
        self.stop_plotting()
        self.worker.stop()
        self.worker_thread.join()
        self.context.term()
        event.accept()

    def on_mouse_move(self, pos):
        mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
        x = mouse_point.x()
        y = mouse_point.y()
        self.vline.setPos(x)
        self.hline.setPos(y)
        self.label.setText(f"x={x:.2f} Hz, y={y:.2f} dB")
        self.label.setPos(x, y)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()