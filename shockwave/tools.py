import os
import numpy as np
from absl import logging
import cv2


def makeFolder(folderName: str):
    """
    make folderName if not exist
    Parameters
    ----------
    folderName string

    Returns create non-existed folder
    -------

    """
    if not os.path.exists(folderName):
        os.mkdir(folderName)
        logging.info('Create folder {}'.format(folderName))
    else:
        # logging.info('folder {} exist'.format(folderName))
        pass


def fileLists(folder: str, delimiter="") -> list:
    """
    return list of the filtered delimited files in folder
    :param folder:
    :param delimiter:
    :return:
    """
    return sorted([x for x in os.listdir(folder) if x.endswith(delimiter) or x.startswith(delimiter)])
    # return sorted([x for x in os.listdir(folder)])


def rescale_image(imgIn: np.ndarray, bitDepth: int = 8) -> np.ndarray:
    """
    rescale img to 8bit image
    @param imgIn:
    @param bitDepth:
    @return: image array
    """
    rows, cols = imgIn.shape
    imgIn = np.double(imgIn)
    imgMax = np.max(imgIn)
    imgMin = np.min(imgIn)
    imgOut = np.zeros_like(imgIn)
    imgOut = (imgIn - imgMin) / (imgMax - imgMin) * ((2 ** bitDepth) - 1)
    return imgOut


def centroid(x: np.ndarray) -> np.double:
    """
    function to calculate the centroid of the signal
    @param x:
    @return:
    """
    logging.debug(f"numerator is {np.sum(x * (1 + np.arange(len(x))))}")
    logging.debug(f"denominator is {np.sum(x)}")
    return np.sum(x * (1 + np.arange(len(x)))) / np.sum(x)


def cell_detection(img: np.ndarray, gaussianKernel: tuple = (3, 3), imgMin: int = 0, imgMax: int = 255, boxX=30,
                   boxY=30):
    """
    :param img:
    :param gaussianKernel:
    :param imgMin:
    :param imgMax:
    :param boxX:
    :param boxY:
    :return:
    """

    # Gaussian blur to remove the hot/dark pixel
    blur = cv2.GaussianBlur(img, gaussianKernel, 0)

    # threshold
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    result = np.zeros((100, 4))
    for contour in contours:
        # Obtain the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # if w > boxX or h > boxY:
        if w > boxX and h > boxY:
            result[count, 0:6] = np.array([x, y, w, h])
            count += 1
    return np.uint16(result[:count - 1, :])
