import os
import numpy as np
from absl import logging
from matplotlib import pyplot as plt
from cellpose import models
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


def detect_cells(image, diameter=120, model=models.Cellpose(model_type='cyto')):
    channels = [0, 0]
    masks, _, _, _ = model.eval(image, diameter=diameter, channels=channels)
    return masks


def cell_info(masks: np.ndarray, img: np.ndarray) -> np.ndarray:
    """

    :param masks:
    :param img:
    :return:
    """
    num_cells = masks.max()
    locations = np.zeros((num_cells, 9))
    for i in range(1, num_cells + 1):
        mask = masks == i
        ymin, xmin = mask.nonzero()[0].min(), mask.nonzero()[1].min()
        ymax, xmax = mask.nonzero()[0].max(), mask.nonzero()[1].max()
        xMean = np.mean(mask, 0)
        yMean = np.mean(mask, 1)
        locations[i - 1, 0] = i
        locations[i - 1, 1] = centroid(xMean)
        locations[i - 1, 2] = centroid(yMean)
        locations[i - 1, 3] = np.sum(img*mask)/np.sum(mask)-np.min(np.ravel(img))
        locations[i - 1, 4] = np.min(np.ravel(img))
        locations[i - 1, 5] = xmin
        locations[i - 1, 6] = ymin
        locations[i - 1, 7] = xmax
        locations[i - 1, 8] = ymax
    return locations


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


def peak_location(dataIn: np.ndarray) -> np.ndarray:
    return np.argmax(dataIn)


def peak_val(dataIn: np.ndarray) -> np.ndarray:
    return np.max(np.ravel(dataIn))


def full_width_half_maximum(dataIn: np.ndarray) -> np.ndarray:
    idxMax = np.argmax(dataIn)
    halfMax = dataIn[idxMax] / 2
    left = (dataIn[:idxMax - 1] >= halfMax)
    right = (dataIn[idxMax + 1:] >= halfMax)
    print("sum of left is {}".format(np.sum(left)))
    print("sum of right is {}".format(np.sum(right)))
    leftIdx = 0
    rightIdx = 0
    if np.sum(left) == 0:
        # print(" left=0 index is {}".format(idxMax-1))
        leftIdx = idxMax - 1
    if np.sum(left) > 0 & np.sum(left) < len(dataIn[:idxMax - 1]):
        # print(" left>0 index is {}".format((left * dataIn[:idxMax - 1] != 0).argmax(axis=0)))
        leftIdx = (left * dataIn[:idxMax - 1] != 0).argmax(axis=0)
    if np.sum(right) > 0 & np.sum(right) < len(dataIn[idxMax + 1:]):
        # print(" right is {}".format(right * dataIn[idxMax + 1:]))
        print(" right index is {}".format(
            len(dataIn[idxMax + 1:]) - ((np.flipud(right * dataIn[idxMax + 1:])) != 0).argmax(axis=0)))
        rightIdx = len(dataIn[idxMax + 1:]) - ((np.flipud(right * dataIn[idxMax + 1:])) != 0).argmax(axis=0)
    if np.sum(right) == len(dataIn[idxMax + 1:]):
        # print(" right index is {}".format(len(dataIn[idxMax + 1:])))
        rightIdx = len(dataIn[idxMax + 1:])
    leftLinearFit = linear_fit([dataIn[leftIdx], leftIdx], [dataIn[leftIdx - 1], leftIdx - 1], halfMax)
    rightLinearFit = linear_fit([dataIn[idxMax + rightIdx], idxMax + rightIdx],
                                [dataIn[idxMax + rightIdx - 1], idxMax + rightIdx - 1], halfMax)
    # return rightLinearFit - leftLinearFit
    # print("width is {}".format(rightLinearFit-leftLinearFit))
    # plt.figure(figsize=(12, 3))
    # plt.subplot(131)
    # plt.plot(dataIn, '-o')
    # plt.plot(halfMax * np.ones(len(dataIn), ), '-r', lw=2)
    # plt.grid()
    # plt.subplot(132)
    # plt.plot(left, '-o')
    # # plt.plot(halfMax * np.ones(len(dataIn), ), '-r', lw=2)
    # plt.grid()
    # plt.subplot(133)
    # plt.plot(right, '-o')
    # # plt.plot(halfMax * np.ones(len(dataIn), ), '-r', lw=2)
    # # plt.grid()
    # plt.show()

    # if (np.sum(left) > 0) & (np.sum(right) > 0):
    #     leftIdx = (left != 0).argmax(axis=0)
    #     rightIdx = (right != 0).argmax(axis=0)
    #     print(leftIdx, rightIdx)
    print("width is {}".format(rightLinearFit - leftLinearFit + idxMax))
    return rightLinearFit - leftLinearFit + idxMax
    # if (np.sum(left) == 0) & (np.sum(right) > 0):
    #     print(right)
    #     rightIdx = (right != 0).argmax(axis=0)
    #     print("rightIdx is {}".format(rightIdx))
    #     rightLinearFit = linear_fit([dataIn[rightIdx], rightIdx], [dataIn[rightIdx - 1], rightIdx - 1], halfMax)
    #     return rightLinearFit-idxMax-.5


def linear_fit(pt1, pt2, target):
    p = np.polyfit([pt1[0], pt2[0]], [pt1[1], pt2[1]], 1)
    return np.polyval(p, target)
