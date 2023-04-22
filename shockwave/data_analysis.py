import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
import time
import shutil
from datetime import datetime, timedelta
from ISP import tools
from absl import app
from absl import flags
from absl import logging
from ISP import tools


FLAGS = flags.FLAGS
flags.DEFINE_string('folder',
                    r'C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922 FOV5\Fluo4',
                    'Stuart SFR raw image filename')


def main(argv):
    folderName = FLAGS.folder
    logging.debug(folderName)
    fileNames = tools.fileLists(folderName, delimiter="tif")
    logging.debug(fileNames)
    signal = np.zeros((len(fileNames), 1))
    for idx, fileName in enumerate(fileNames[49:50]):
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        logging.info("{}, {}, {:.3f}".format(fileName, temp.shape, np.mean(np.ravel(temp))))
        signal[idx, 0] = np.mean(np.ravel(temp))
        # Normalize pixel values to 0-255 range
        img = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        # roi detection
        rois = tools.cell_detection(img)
        logging.info(rois)

        for roi in rois:
            img = cv2.rectangle(img, (roi[0], roi[1]), (roi[0]+roi[2], roi[1]+roi[3]), (255, 0, 0), thickness=2)
        cv2.imwrite("brightness.png", img)

    result = np.zeros((len(fileNames), len(rois)))
    for idy, fileName in enumerate(fileNames[:]):
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        for idx, roi in enumerate(rois):
            x, y, w, h = roi
            cropImg = temp[y: y + h, x:x + w]
            result[idy, idx] = np.mean(np.ravel(cropImg))
            # logging.info("{}, {}, {:.3f}".format(fileName, idx, result[idy, idx]))
        logging.info(result[idy, :])
    np.savetxt("ROIs.csv", rois, delimiter=',')
    np.savetxt("result.csv", result, delimiter=',')


if __name__ == '__main__':
    app.run(main)
