import os
import sys
import numpy as np
import cv2
from absl import app
from absl import flags
from absl import logging
from cellpose import models, plot
import tools

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    r"C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4",
                    "Folder name")
flags.DEFINE_integer("diameter", 120, "Custom diameter value (in pixels) used for the cellpose model")


def main(argv):
    global rois
    folderName = FLAGS.folder
    destFolder = os.path.join(folderName, "output")
    tools.makeFolder(destFolder)
    destFolder = os.path.join(destFolder, "cell_search")
    tools.makeFolder(destFolder)
    logging.debug(folderName)
    fileNames = tools.fileLists(folderName, delimiter="tif")
    logging.debug(fileNames)

    logging.info("{} Start image analysis {}".format(50 * "=", 50 * "="))
    logging.info("{} detect the brightest frame {}".format(50 * "-", 44 * "-"))
    for idx, fileName in enumerate(fileNames[:]):
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        img = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        masks = tools.detect_cells(img, diameter=120, model=models.Cellpose(model_type="cyto"))
        num_cells = masks.max()
        cellInfo = tools.cell_info(masks, temp)
        logging.info("idx->{},filename->{},numberOfCells->{}".format(idx, fileName, num_cells))
        np.savetxt(os.path.join(destFolder, "{}.csv".format(fileName[:-4])), cellInfo, delimiter=",",
                   header="index,x,y,signal,background,xmin,ymin,xmax,ymax", comments="")
    logging.info("{} Finish image analysis {}".format(49 * "=", 49 * "="))


if __name__ == "__main__":
    app.run(main)
