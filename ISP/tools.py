import os
import numpy as np
from absl import logging


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
