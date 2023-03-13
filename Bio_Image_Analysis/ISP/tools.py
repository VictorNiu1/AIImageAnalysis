import numpy as np
from absl import logging


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
    logging.debug(f"numerator is {np.sum(x*(1+np.arange(len(x))))}")
    logging.debug(f"denominator is {np.sum(x)}")
    return np.sum(x*(1+np.arange(len(x))))/np.sum(x)
