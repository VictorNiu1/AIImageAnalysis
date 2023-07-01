import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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
                    r'C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data_visualization',
                    'Stuart SFR raw image filename')


def main(argv):
    folderName = FLAGS.folder
    df = pd.DataFrame()
    for root, dirs, files in os.walk(folderName, topdown=False):
        for name in files:
            if name.endswith("brightness.csv"):
                fullFileName = os.path.join(root, name)
                fullFileStr = fullFileName.split("\\")
                fovNumber = fullFileStr[-4]
                cellNumber = fullFileStr[-3]
                column = "{}_{}".format(fovNumber, cellNumber)
                logging.info(fullFileName)
                temp = pd.read_csv(fullFileName)
                df[column] = temp["signal"]

    df["Time"] = temp["Time"]
    df["Time"] = pd.to_datetime(df["Time"], format="%Y%m%d %H:%M:%S")
    start = df.iloc[0]["Time"]
    df["timeDelta"] = df["Time"].apply(lambda x: (x - start)/np.timedelta64(1, "m")).astype("int64")
    cols = list(df.columns)
    cols = [cols[-2]] + [cols[-1]] + cols[:-2]
    df = df[cols]
    df.to_csv("result.csv", index=False)


if __name__ == '__main__':
    app.run(main)
