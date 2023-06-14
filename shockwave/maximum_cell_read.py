import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import tools
from absl import app
from absl import flags
from absl import logging
import cv2

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    r"C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4\output\cell_search",
                    "Folder name")


def main(argv):
    folderName = FLAGS.folder
    fileNames = tools.fileLists(folderName, delimiter="csv")
    df = pd.DataFrame()
    for idx, fileName in enumerate(fileNames[:]):
        if idx % 50 == 0:
            logging.info("filename is {}".format(fileName[:-4]))
        temp = pd.read_csv(os.path.join(folderName, fileName))
        temp["file"] = fileName[:-4]
        df = pd.concat([df, temp])

    columns = df.columns
    fileSns = df["file"].unique()
    cellCounts = np.zeros(len(fileSns), )
    for idx, fileSn in enumerate(fileSns):
        cellCounts[idx] = len(df[df["file"] == fileSn])
    maxIdx = np.argmax(cellCounts)
    with open(os.path.join(folderName[:-12], "max_cell_frame.csv"), "w") as fp:
        fp.write("max_cell_frame\n")
        fp.write(str(maxIdx)+"\n")
    logging.info("the maximum cell happened at frame {}".format(maxIdx))

    plt.rcParams["font.size"] = "14"
    style = "seaborn-v0_8-darkgrid"
    plt.style.use(style)
    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    ax.plot(cellCounts, "-")
    ax.plot(maxIdx, cellCounts[maxIdx], "-h", markersize=8)
    ax.axvline(maxIdx, color="r", linestyle=":", lw=1.5)
    ax.text(maxIdx + 5, cellCounts[maxIdx], str(maxIdx), color="r")
    ax.set_xlabel("Frame")
    ax.set_ylabel("cell count")
    plt.savefig(os.path.join(folderName, "cell_count.png"), dpi=150)
    plt.close()


if __name__ == "__main__":
    app.run(main)
