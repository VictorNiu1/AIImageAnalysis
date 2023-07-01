import os
import sys
import numpy as np
import cv2
from absl import app
from absl import flags
from absl import logging
import tools
from matplotlib import pyplot as plt

FLAGS = flags.FLAGS
flags.DEFINE_string('folder',
                    r'C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4',
                    'Folder name')


def main(argv):
    plt.rcParams['font.size'] = '14'
    style = 'seaborn-v0_8-darkgrid'
    plt.style.use(style)

    folderName = FLAGS.folder
    destFolder = os.path.join(folderName, "output")
    tools.makeFolder(destFolder)
    logging.debug(folderName)
    fileNames = tools.fileLists(folderName, delimiter="tif")
    logging.debug(fileNames)

    logging.info("{} Start image analysis {}".format(50 * "=", 50 * "="))
    logging.info("{} Get the dark background {}".format(50 * "-", 47 * "-"))
    backGroundThreshold = 0
    backGroundResults = np.zeros((len(fileNames), 2))
    for idx, fileName in enumerate(fileNames[:]):
        if idx % 100 == 0:
            logging.info(fileName)
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        backGround = np.min(temp) * (1 + backGroundThreshold / 100)
        backGroundResults[idx, 0] = idx+1
        backGroundResults[idx, 1] = backGround

    header = "index,background"
    np.savetxt(os.path.join(destFolder, "background.csv"), backGroundResults,
               delimiter=',', header=header, comments="")
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.plot(backGroundResults[:, 1], '-o', linewidth=3.0)
    ax.set_title('Background signal')
    ax.set_xlabel('Frame Index')
    ax.set_ylabel('Signal [DN]')
    plt.savefig(os.path.join(folderName, "output", "background.png"), dpi=150)
    plt.close()
    # plt.show()
    logging.info("{} Finish image analysis {}".format(49 * "=", 49 * "="))


if __name__ == '__main__':
    app.run(main)
