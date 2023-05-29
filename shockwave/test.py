import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
from absl import app
from absl import flags
from absl import logging
import tools
import csv

rois_w_header = []

file = open("data/101922 FOV5/Fluo4/output/ROIs.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

rois = data[1:]

'''

file = open("data/101922 FOV5/Fluo4/output/brightness.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

result_0 = data[1:]

result = np.zeros((len(result_0), len(rois) + 1))
i = 0
j = 0
for r in result_0:
    for v in r:
        print(v)
        result[i, j] = v
        j += 1
    i += 1
    j = 0
''' 

# Load the CSV file and import the header rows
header_data = np.genfromtxt('data/101922 FOV5/Fluo4/output/brightness.csv', delimiter=',', dtype=str, max_rows=1)

# Load the CSV file and import the data rows, skipping the header
result = np.genfromtxt('data/101922 FOV5/Fluo4/output/brightness.csv', delimiter=',', skip_header=1)

row = 4
col = int(np.ceil(len(rois) / row))

print(row, col)
plt.figure(figsize=(int(row * 3), col * 2))
for index in range(len(rois)):
    if col > row:
        plt.subplot(col, row, index + 1)
    else:
        plt.subplot(row, col, index + 1)
    #print(result[index])
    #print(result[:, 0])
    
    plt.plot(result[:, 0], result[:, index + 1])
    plt.grid(True)
    plt.title("ROI_{:0d}".format(index + 1))
    plt.xlabel("frame")
    plt.ylabel("signal [DN]")
    plt.tight_layout()
plt.tight_layout()
plt.show()

plt.close()

logging.info("{} Finish image analysis {}".format(49 * "=", 49 * "="))