import time
import json
import random
import sys
import numpy as np

def generate_spectroscopy_data(num_points=1000, num_peaks=5, noise_level=0.1):
    x = np.linspace(0, 100, num_points)
    y = np.zeros(num_points)
    
    for _ in range(num_peaks):
        peak_center = random.uniform(10, 90)
        peak_height = random.uniform(1, 10)
        peak_width = random.uniform(1, 5)
        y += peak_height * np.exp(-((x - peak_center) ** 2) / (2 * peak_width ** 2))
    
    y += noise_level * np.random.normal(size=num_points)
    return x.tolist(), y.tolist()

if __name__ == "__main__":
    while True:
        x, y = generate_spectroscopy_data()
        data = {
            'x': x,
            'y': y
        }
        print(json.dumps(data))
        sys.stdout.flush()
        time.sleep(1)