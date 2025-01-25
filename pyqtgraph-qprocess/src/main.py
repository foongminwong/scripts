import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QProcess, QByteArray, QTimer
import pyqtgraph as pg
import json

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Plotting App via QProcess")
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.x = []
        self.y = []

        # Add vertical and horizontal lines
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('g'))
        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('g'))
        self.plot_widget.addItem(self.vline, ignoreBounds=True)
        self.plot_widget.addItem(self.hline, ignoreBounds=True)

        # Add text item to display coordinates
        self.text_item = pg.TextItem("", anchor=(0, 1))
        self.plot_widget.addItem(self.text_item)

        # Connect mouse move event
        self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)

    def update_plot(self, x, y):
        self.x = x
        self.y = y
        self.plot_widget.plot(self.x, self.y, pen=pg.mkPen('r'), clear=True)

    def mouse_moved(self, pos):
        mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
        x = mouse_point.x()
        y = mouse_point.y()
        self.vline.setPos(x)
        self.hline.setPos(y)
        self.text_item.setText(f"x={x:.2f}, y={y:.2f}")
        self.text_item.setPos(x, y)

def main():
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()

    # Set up QProcess to receive data from plotworker
    process = QProcess()
    process.setProgram("python")
    plotworker_path = os.path.join(os.path.dirname(__file__), "plotworker.py")
    process.setArguments([plotworker_path])
    process.start()

    buffer = []

    def read_output():
        while process.canReadLine():
            line = process.readLine()
            data = json.loads(str(line, 'utf-8'))
            buffer.append(data)

    process.readyReadStandardOutput.connect(read_output)

    def update_plot():
        if buffer:
            data = buffer.pop(0)
            window.update_plot(data['x'], data['y'])

    timer = QTimer()
    timer.timeout.connect(update_plot)
    timer.start(50)  # Update plot every 50 ms

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()