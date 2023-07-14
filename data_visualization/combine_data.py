import os
import numpy as np
import pandas as pd
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS
flags.DEFINE_string('folder',
                    r'C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\results\04112023 Tong KO 5787 5713\04112023 Tong KO 5787 5713\Dish1 KO 5713 COMPLETED\FOV4 6 cells 50mW\output',
                    'Stuart SFR raw image filename')


def main(argv):
    folderName = FLAGS.folder
    df = pd.DataFrame()
    temp = None
    for root, dirs, files in os.walk(folderName, topdown=False):
        for name in files:
            if name.endswith(".csv"):
                fullFileName = os.path.join(root, name)
                fullFileStr = fullFileName.split("\\")
                fovNumber = fullFileStr[-4]
                cellNumber = fullFileStr[-3]
                column = "{}_{}".format(fovNumber, cellNumber)
                logging.info(fullFileName)
                temp = pd.read_csv(fullFileName)
                df[column] = temp["signal"]

    if temp is not None:
        df["Time"] = temp["Time"]
        df["Time"] = pd.to_datetime(df["Time"], format="%Y-%m-%d %H:%M:%S")
        start = df.iloc[0]["Time"]
        df["timeDelta"] = df["Time"].apply(lambda x: (x - start) / np.timedelta64(1, "m")).astype("int64")
        cols = list(df.columns)
        cols = [cols[-2]] + [cols[-1]] + cols[:-2]
        df = df[cols]
        df.to_csv(r"C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\results\04112023 Tong KO 5787 5713\04112023 Tong KO 5787 5713\Dish1 KO 5713 COMPLETED\FOV4 6 cells 50mW\output\output\result.csv", index=False)


        


if __name__ == '__main__':
    app.run(main)