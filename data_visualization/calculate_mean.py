import os
import numpy as np
import pandas as pd
import cv2
import time
import shutil
from datetime import datetime, timedelta
from absl import app
from absl import flags
from absl import logging
from ISP import tools


FLAGS = flags.FLAGS
flags.DEFINE_string('folder',
                    r'C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data_visualization\FOV_5',
                    'Stuart SFR raw image filename')


def main(argv):
    folderName = FLAGS.folder
    subFolderNames = tools.fileLists(folderName)
    logging.debug(subFolderNames)
    for subFolderName in subFolderNames:
        destFolder = os.path.join(folderName, subFolderName, "output")
        timeStamp = []
        tools.makeFolder(destFolder)
        fileNames = tools.fileLists(os.path.join(folderName, subFolderName), delimiter="tif")
        signal = np.zeros((len(fileNames), 1))
        for index, fileName in enumerate(fileNames):
            fileNameStr = fileName.split("_")
            timeStamp.append(datetime.strptime(
                "20{}{}{} {}{}{}".format(fileNameStr[2], fileNameStr[0], fileNameStr[1], fileNameStr[3][:2],
                                         fileNameStr[3][3:5], fileNameStr[4][:2]), "%Y%m%d %H%M%S"))
            img = cv2.imread(os.path.join(folderName, subFolderName, fileName), 0)
            signal[index, 0] = "{:.3f}".format(np.mean(img))
            logging.info("{},{},{}".format(subFolderName, fileName, signal[index, 0]))
        df = pd.DataFrame(timeStamp, columns=["Time"])
        df["signal"] = signal

        df.to_csv(os.path.join(destFolder, "{}_brightness.csv".format(subFolderName)),index=False)


if __name__ == '__main__':
    app.run(main)
