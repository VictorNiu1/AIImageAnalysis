"""
# Laser cutting signal detection on single cell
#
# USAGE: python3.8 .\single_DNA_brightness_analysis_20230310.py [flags]
# flags:
#
# .\single_DNA_brightness_analysis_20230310.py:
#   --folder: Single DNA folder
#     (default: 'C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\Bio_Imag
#     e_Analysis\\U2OS_53KO_5979GFP_FOV3')
#   --threshPercentage: the percentage is an integer between 0 and 100
#     (default: '96')
#     (an integer)
#
# The result saved into the "output" under the folder which contains all images.
# 1. Montage of all image (overlay the origin image and detected line)
# 2. Brightness vs. Time graph
# 3. Brightness vs. Time "csv" text result
"""
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    r"C:\Users\changfan\Documents\GitHub\AIImageAnalysis\zeiss\Cell104\post",
                    "Multi-cell DNA folder")
flags.DEFINE_integer("average_x", 48, "the percentage is an integer between 0 and 100")
flags.DEFINE_integer("average_y", 48, "the percentage is an integer between 0 and 100")


def average_Image(img: np.ndarray, kernalX: int = 48, kernalY: int = 48) -> np.ndarray:
    rows, cols = img.shape
    result = np.zeros((rows // kernalX, cols // kernalY))
    for idx in range(rows // kernalX):
        for idy in range(cols // kernalY):
            cropImg = img[kernalX * idx:kernalX * (idx + 1), kernalY * idy:kernalY * (idy + 1)]
            result[idx, idy] = np.mean(cropImg)
    return result


def cell_detection(img: np.ndarray, gaussianKernal: tuple = (3, 3), imgMin: int = 0, imgMax: int = 255, boxX=40,
                   boxY=40):
    """

    :param img:
    :param gaussianKernal:
    :param imgMin:
    :param imgMax:
    :param boxX:
    :param boxY:
    :return:
    """

    # Gaussian blur to remove the hot/dark pixel
    blur = cv2.GaussianBlur(img, gaussianKernal, 0)

    # threshold
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    result = np.zeros((1000, 4))
    for contour in contours:
        # Obtain the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # if w > boxX or h > boxY:
        if w > boxX and h > boxY:
            result[count, 0:6] = np.array([x, y, w, h])
            count += 1
    return np.uint16(result[:count - 1, :])


def overlay_plot(img, rois, filename="test.png"):
    plt.figure()
    plt.imshow(img, cmap='gray')
    for idx, roi in enumerate(rois):
        x, y, w, h = roi
        plt.plot(x + w / 2, y + h / 2, 'r+', markersize=10)
        plt.text(x + w / 2 - 25, y + h / 2 - 15, 'ROI_{}'.format(idx + 1), color='b')
        plt.plot([x, x + w, x + w, x, x], [y, y, y + h, y + h, y], '-r')
    plt.title(filename[:-4])
    plt.tight_layout()
    # plt.savefig("{}_overlay.png".format(filename[:-4]), dpi=150)
    # plt.close()


def main(argv):
    font = {'family': 'serif',
            'color': 'white',
            'weight': 'normal',
            'size': 12,
            }
    global rows, cols, kernalX, kernalY
    rows = 2304
    cols = 2304
    kernalX = 96
    kernalY = 96
    logging.set_verbosity(logging.INFO)
    plt.rcParams['font.size'] = '8'
    style = 'seaborn-v0_8-darkgrid'
    plt.style.use(style)

    logging.info("================== Start data analysis =================")

    # get all tif file to process
    folderName = FLAGS.folder
    destFolder = os.path.join(folderName, 'output')
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)
    fileNames = sorted([x for x in os.listdir(folderName) if x.endswith("tif") | x.endswith("jpg")])

    # calculate the moving average of image
    for idx, fileName in enumerate(fileNames[:]):
        logging.info("{},{}".format(idx, fileName))
        temp = cv2.imread(os.path.join(folderName, fileName), -1)
        # img = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        #
        # # roi detection
        # rois = cell_detection(255-img)
        # logging.info(len(rois))
        # logging.info(rois)
        # overlay_plot(255-img, rois)
        # plt.show()
        img2 = average_Image(temp, kernalX=kernalX, kernalY=kernalY)
        np.savetxt(os.path.join(folderName, "output", "{}.csv".format(fileName[:-4])), img2, delimiter=',')

    # # plot the result
    # # for signal in ["c001", "c002", "c003"]:
    # plt.figure(figsize=(12, 12))
    # plt.imshow(cv2.imread(os.path.join(folderName, r"Cell 104 Pre_t001_c001.tif"), -1), cmap='gray')
    for signal in ["c001"]:
        resultFiles = [x for x in os.listdir(os.path.join(folderName, "output")) if x.endswith("csv") and signal in x]
        results = np.zeros((rows // kernalX, cols // kernalY, len(resultFiles)))
        for idx, resultFile in enumerate(resultFiles[:]):
            logging.info("{},{}".format(idx, resultFile))
            results[:, :, idx] = np.loadtxt(os.path.join(folderName, "output", resultFile), delimiter=",", dtype=float)
        for idx in range(24):
            plt.figure(figsize=(16, 6))
            for idy in range(24):
                logicSignal = np.diff(results[idx, idy, 20:])
                if sum(logicSignal > 0) | sum(logicSignal < -400):
                    logging.info("idx={},x={}, idy={}, y={}".format(idx, 96 * (idx + 1), idy, 96 * (idy + 1)))
                    #             plt.plot(96*(idy+1), 96*(idx+1), 'o', markersize=12)
                    #             plt.text(96*(idy+1), 96*(idx+1)+20, "({},{})".format(96*(idx+1), 96*(idy+1)), fontdict=font)
                    #     logging.info(50*'-')
                    # plt.show()
                    plt.subplot(121)
                    plt.plot(results[idx, idy, 20:], '-o', label="x={},y={}".format(96 * (idx + 1), 96 * (idy + 1)))
                    plt.legend()
                    plt.tight_layout()
                    plt.subplot(122)
                    plt.plot(np.diff(results[idx, idy, 20:]), '-o',
                             label="x={},y={}".format(96 * (idx + 1), 96 * (idy + 1)))
                    plt.legend()
                    plt.tight_layout()
            plt.savefig(os.path.join(folderName, "output", "104_pre_idx_{}_{}.png".format(idx + 1, signal)), dpi=150)
            plt.close()
            logging.info(50 * '-')
    logging.info("================= Finish data analysis =================")


if __name__ == "__main__":
    app.run(main)
