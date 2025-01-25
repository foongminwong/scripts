# PyQt Plotting App via QProcess

This project is a simple data visualization application built using PyQt5 and PyQtGraph. It generates simulated data and displays it in real-time using a graphical user interface.

## Project Structure
```
pyqtgraph-plotter
├── src
│   ├── main.py          # Entry point of the application
│   └── plotworker.py    # Generates simulated data
├── requirements.txt      # Lists project dependencies
└── README.md             # Project documentation
```

## Requirements

To run this project, you need to install the following dependencies:

- PyQt5
- PyQtGraph

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

   ```
   git clone <repository-url>
   cd pyqtgraph-plotter
   ```

2. Install the required dependencies as mentioned above.

3. Run the application:

   ```
   python src/main.py
   ```

The application will start, and you will see a window displaying the real-time plot of the simulated data.