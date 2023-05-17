import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
from absl import app
from absl import flags
from absl import logging
import tools

FLAGS = flags.FLAGS
flags.DEFINE_string('folder',
                    r'C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922 FOV5\Fluo4',
                    'Stuart SFR raw image filename')


def main(argv):
    global rois
    plt.rcParams['font.size'] = '14'
    style = 'seaborn-v0_8-darkgrid'
    plt.style.use(style)
    folderName = FLAGS.folder
    destFolder = os.path.join(folderName, "output")
    tools.makeFolder(destFolder)
    logging.debug(folderName)
    fileNames = tools.fileLists(folderName, delimiter="tif")
    logging.debug(fileNames)

    # detect the starting point of the movie
    logging.info("{} Start image analysis {}".format(50 * "=", 50 * "="))
    logging.info("{} detect the brightest frame {}".format(50 * "-", 44 * "-"))
    maxSignal = 0
    startIdx = 0
    for idx, fileName in enumerate(fileNames):
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        meanValue = np.mean(np.ravel(temp))
        logging.debug("{},{}".format(idx, meanValue))
        if meanValue >= maxSignal:
            maxSignal = meanValue
            startIdx = idx
    logging.info("The index of maximum frame is -> {}".format(startIdx))

    logging.info("{} detect cell on the brightest frame {}".format(50 * "-", 36 * "-"))
    # open the frame with the maximum average signal
    temp = cv2.imread(os.path.join(folderName, fileNames[startIdx]), -1)

    # Normalize pixel values to 0-255 range
    img = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # roi detection
    rois = tools.cell_detection(img)
    np.savetxt(os.path.join(destFolder, "ROIs.csv"), rois, delimiter=',', header="x,y,w,h", comments="")
    logging.info("save the roi coordinator to   -> {}".format(os.path.join(destFolder, "ROIs.csv")))

    # logging.info(rois)
    rows, cols = img.shape

    # create rgb image
    img2 = np.zeros((rows, cols, 3))
    for index in range(3):
        img2[:, :, index] = img
    for index, roi in enumerate(rois):
        img = cv2.rectangle(img2, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 0, 255), thickness=2)
        img = cv2.putText(img2, text="Roi_{:02d}".format(index + 1), org=(roi[0], roi[1] - 10),
                          fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                          fontScale=.4, color=(0, 255, 0), thickness=1)
    cv2.imwrite(os.path.join(destFolder, "roi.png"), img)
    logging.info("save the roi image to         -> {}".format(os.path.join(destFolder, "roi.png")))

    logging.info("{} calculate the roi signal on each frame {}".format(50 * "-", 32 * "-"))
    # calculate the brightness on each roi and frame
    result = np.zeros((len(fileNames), len(rois) + 1))
    for idy, fileName in enumerate(fileNames[:]):
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        result[idy, 0] = idy + 1
        for idx, roi in enumerate(rois):
            x, y, w, h = roi
            cropImg = temp[y: y + h, x:x + w]
            result[idy, idx + 1] = np.mean(np.ravel(cropImg))
            # logging.info("{}, {}, {:.3f}".format(fileName, idx, result[idy, idx]))
    header = "index,"
    for index in range(len(rois)):
        header += "roi_{:0d},".format(index + 1)
    np.savetxt(os.path.join(destFolder, "brightness.csv"), result, delimiter=',', header=header, comments="")
    logging.info("save the roi signal to        -> {}".format(os.path.join(destFolder, "brightness.csv")))
    # plot brightness on each roi
    row = 4
    col = int(np.ceil(len(rois) / row))

    plt.figure(figsize=(int(row * 3), col * 2))
    for index in range(len(rois)):
        if col > row:
            plt.subplot(col, row, index + 1)
        else:
            plt.subplot(row, col, index + 1)
        plt.plot(result[:, 0], result[:, index + 1])
        plt.grid(True)
        plt.title("ROI_{:0d}".format(index + 1))
        plt.xlabel("frame")
        plt.ylabel("signal [DN]")
        plt.tight_layout()
    plt.tight_layout()
    plt.savefig(os.path.join(folderName, "output", "brightness.png"), dpi=150)
    plt.close()
    logging.info("save the shock wave image to -> {}".format(os.path.join(folderName, "output", "brightness.png")))
    logging.info("{} Finish image analysis {}".format(49 * "=", 49 * "="))


if __name__ == '__main__':
    app.run(main)
