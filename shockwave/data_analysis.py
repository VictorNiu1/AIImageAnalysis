import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
from absl import app
from absl import flags
from absl import logging
from cellpose import models, plot
import tools

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    r"C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4",
                    "Folder name")
flags.DEFINE_string("fileName",
                    r"C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4\output\max_cell_frame.csv",
                    "maximum label frame")


def main(argv):
    global rois
    folderName = FLAGS.folder
    logging.debug(folderName)

    destFolder = os.path.join(folderName, "output")
    tools.makeFolder(destFolder)

    maxFrameFileName = FLAGS.fileName
    maxFrame = np.int16(np.genfromtxt(maxFrameFileName, skip_header=1))
    logging.debug(maxFrame)

    fileNames = tools.fileLists(folderName, delimiter="tif")
    logging.debug(fileNames)
    #
    logging.info("{} Start image analysis {}".format(50 * "=", 50 * "="))
    logging.info("{} detect the brightest frame {}".format(50 * "-", 44 * "-"))

    fileName = fileNames[maxFrame]
    temp = cv2.imread(os.path.join(folderName, fileName), -1)
    img = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    masks = tools.detect_cells(img, diameter=120, model=models.Cellpose(model_type="cyto"))
    cellInfo = tools.cell_info(masks, temp)

    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }
    plt.figure(figsize=(8, 8))
    plt.imshow(masks, cmap="gray")
    for idx, cell in enumerate(cellInfo):
        plt.text(cell[1], cell[2], "roi_{}".format(idx),  fontdict=font)
    plt.title(fileName)
    plt.tight_layout()
    plt.savefig(os.path.join(destFolder, "mask.png"), dpi=150)
    plt.close()
    num_cells = masks.max()
    result = pd.DataFrame()
    for idx, fileName in enumerate(fileNames[:]):
        if idx % 50 == 0:
            logging.info("{}".format(fileName))
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        background = temp.min()
        df = pd.DataFrame()
        df['index'] = [idx]
        df['background'] = [background]
        for roiIdx in range(0, num_cells):
            logging.debug("{}".format(roiIdx))
            mask = (masks == roiIdx)
            mask = mask.astype(int)
            logging.debug("{}, {}".format(roiIdx, np.sum(mask)))
            filterImg = temp * mask
            df["roi_{}".format(roiIdx)] = [np.sum(filterImg)/np.sum(mask)]
        result = pd.concat([result, df])
    result.to_csv(os.path.join(destFolder, "final_brightness.csv"), index=False)
    logging.debug("\n{}".format(result))
    logging.info("{} Finish image analysis {}".format(49 * "=", 49 * "="))


if __name__ == "__main__":
    app.run(main)
