"""
Laser cutting signal detection on single cell

USAGE: python3.8 .\single_DNA_brightness_analysis_20230310.py [flags]
flags:

.\single_DNA_brightness_analysis_20230310.py:
  --folder: Single DNA folder
    (default: 'C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\Bio_Imag
    e_Analysis\\U2OS_53KO_5979GFP_FOV3')
  --threshPercentage: the percentage is an integer between 0 and 100
    (default: '96')
    (an integer)

The result saved into the "output" under the folder which contains all images.
1. Montage of all image (overlay the origin image and detected line)
2. Brightness vs. Time graph
3. Brightness vs. Time "csv" text result
"""
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime
import pandas as pd
from ISP import tools
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    os.path.join(os.getcwd(), "U2OS_53KO_5979GFP_FOV3"),
                    "Single DNA folder")
flags.DEFINE_integer("threshPercentage", 96, "the percentage is an integer between 0 and 100")


def brightness_plot(brightness, timeStamp, title="title", fileName="test.png"):
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(timeStamp, brightness, "-o")
    plt.grid(True)
    locator = md.AutoDateLocator()
    formatter = md.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.ylabel("Brightness [DN]")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(fileName, dpi=150)
    plt.close()


def main(argv):
    logging.set_verbosity(logging.INFO)
    plt.rcParams['font.size'] = '14'
    style = 'seaborn-v0_8-darkgrid'
    plt.style.use(style)

    logging.info("================== Start data analysis =================")

    # get threshold percentage
    threshPercentage = int(FLAGS.threshPercentage)

    # get all tif file to process
    folderName = FLAGS.folder
    destFolder = os.path.join(folderName, 'output')
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)
    fileNames = sorted([x for x in os.listdir(folderName) if x.endswith("tif") | x.endswith("jpg")])

    # pre-allocate the brightness and timeStamp array
    brightness = np.zeros(len(fileNames), )
    timeStamp = []

    # set rescale bitdepth to 8
    bitDepth = 8

    # setup 4 subplot on each row
    cols = 4
    rows = int(np.ceil(len(fileNames) / cols))
    logging.debug(f"row is {rows}, col is {cols}")

    # loop through all tif files
    plt.figure(figsize=(32, 32))
    for idx, fileName in enumerate(fileNames[:]):
        logging.info(fileName)
        fileNameStr = fileName.split("_")
        timeStamp.append(datetime.strptime(
            "20{}{}{} {}{}{}".format(fileNameStr[2], fileNameStr[0], fileNameStr[1], fileNameStr[3][:2],
                                     fileNameStr[3][3:5], fileNameStr[4][:2]), "%Y%m%d %H%M%S"))
        # read img
        imgIn = cv2.imread(os.path.join(folderName, fileName), -1)
        logging.debug("the size of image is {}".format(imgIn.shape[0]))

        # rescale image
        imgOut = tools.rescale_image(imgIn, bitDepth=bitDepth)

        mask = imgOut >= ((2 ** bitDepth) - 1) * threshPercentage / 100.

        # overlay mask with the original image
        imgPost = imgIn * mask

        # calculate the brightness
        brightness[idx] = np.sum(imgPost) / np.sum(mask)

        # calculate the centroid of mask
        centerX = int(tools.centroid(np.mean(mask, 1)))
        centerY = int(tools.centroid(np.mean(mask.T, 1)))
        logging.debug("center x is {}, center y is {}".format(centerX, centerY))

        # create pseudo color image
        Red = np.uint8(imgOut) * 0
        Blue = np.uint8(imgOut) * 0
        Green = np.uint8(imgOut)
        pseudoImg = cv2.merge([Blue, Green, Red])
        cropPseudoImg = pseudoImg[centerX - 50:centerX + 50, centerY - 50:centerY + 50]
        cropMask = mask[centerX - 50:centerX + 50, centerY - 50:centerY + 50]

        # generate subplot of image, overlay original image with mask
        plt.subplot(rows, cols, idx + 1)
        # plt.imshow(pseudoImg)
        # plt.imshow(mask, cmap="gray", alpha=.5)
        plt.imshow(cropPseudoImg, aspect='equal')
        plt.imshow(cropMask, cmap="gray", alpha=.5, aspect='equal')
        # plt.imshow(cropMask, cmap="gray", aspect='equal')
        plt.title(fileName)
        plt.grid(False)
        plt.tight_layout()
    plt.savefig(os.path.join(destFolder, "{}_threshpercent_{}.png".format(
        folderName.split("\\")[-1], threshPercentage)), dpi=150)
    # plt.show()
    # plt.close()

    # save timeStamp, brightness result
    df = pd.DataFrame(timeStamp, columns=["Time"])
    df["signal"] = brightness
    df.to_csv(os.path.join(destFolder,
                           "{}_brightness_threshpercent_{}.csv".format(folderName.split("\\")[-1], threshPercentage)),
              index=False)

    # generate brightness plot
    brightness_plot(brightness, timeStamp, title="{}".format(folderName.split("\\")[-1]),
                    fileName=os.path.join(destFolder,
                                          "{}_brightness_threshpercent_{}.png".format(folderName.split("\\")[-1],
                                          threshPercentage)))

    logging.info("================= Finish data analysis =================")


if __name__ == "__main__":
    app.run(main)
