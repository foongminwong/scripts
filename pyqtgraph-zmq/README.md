# PyQt Plotting App via ZeroMQ

## Overview
The PyQt Plotting App via ZeroMQ is a graphical user interface (GUI) application that allows for live plotting of data using PyQt5 and pyqtgraph. It is designed to handle intensive plotting tasks in a separate worker thread, ensuring a responsive user interface.

## Features
- Live data plotting with real-time updates.
- Multi-threaded architecture to handle intensive calculations without freezing the GUI.
- User-friendly interface for interacting with plots.

## Project Structure
```
pyqt-plotting-app
├── src
│   ├── plotworker.py      # Contains the PlotWorker class for data generation and calculations.
│   └── pyqt_zmq.py        # Implements the PyQt GUI for live plotting.
├── requirements.txt        # Lists the project dependencies.
└── README.md               # Documentation for the project.
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pyqt-plotting-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Dependencies
The project requires the following Python packages:
- PyQt5
- pyqtgraph
- pyzmq

Make sure to install these packages using the provided `requirements.txt`.