import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import cv2
import time
import shutil
from datetime import datetime, timedelta
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS


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


def create_random_number_image(rows: int = 512, cols: int = 512, mu: float = 10, sigma: float = 0) -> np.ndarray:
    """
    :param rows:
    :param cols:
    :param mu: mean value of normal distribution
    :param sigma: standard deviation of normal distribution
    :return:
            image dimension rows*columns
    """
    temp = np.random.normal(mu, sigma, rows * cols)
    return temp.reshape((rows, cols))


def main(argv):
    cwd = os.getcwd()
    numOfFov = 5
    numOfCell = 10
    # odd number
    numOfImages = 21
    mu = 22
    sigma = 5
    timeStamp = datetime.now()

    for indexFov in range(numOfFov):
        # delete the previous simulated folder
        if os.path.exists(os.path.join(cwd, "FOV_{}".format(indexFov + 1))):
            shutil.rmtree(os.path.join(cwd, "FOV_{}".format(indexFov + 1)), ignore_errors=True)
        # create FOV folder
        makeFolder(os.path.join(cwd, "FOV_{}".format(indexFov + 1)))

        # create cell folder
        for indexCell in range(numOfCell):
            makeFolder(os.path.join(cwd, "FOV_{}".format(indexFov + 1), "Cell_{:03d}".format(indexCell + 1)))
            dt = timeStamp

            # create gradually increasing image
            for indexImage in range((numOfImages + 1) // 2):
                img = create_random_number_image(mu=mu * (indexImage + 1), sigma=sigma)
                img = np.int8(img)
                dt += timedelta(minutes=3)
                logging.info(os.path.join(cwd, "FOV_{}".format(indexFov + 1), "Cell_{:03d}".format(indexCell + 1),
                                          "{}_Image_{:02d}.tif".format(dt.strftime("%m_%d_%y_%Hh%Mm_%Ss"),
                                          indexImage + 1)))
                cv2.imwrite(os.path.join(cwd, "FOV_{}".format(indexFov + 1), "Cell_{:03d}".format(indexCell + 1),
                                         "{}_Image_{:02d}.tif".format(dt.strftime("%m_%d_%y_%Hh%Mm_%Ss"),
                                         indexImage + 1)), img)

            # create gradually increasing image
            for indexImage in range((numOfImages - 1) // 2):
                img = create_random_number_image(mu=mu * (-indexImage + (numOfImages - 1) // 2), sigma=sigma)
                img = np.int8(img)
                dt += timedelta(minutes=3)
                logging.info(os.path.join(cwd, "FOV_{}".format(indexFov + 1), "Cell_{:03d}".format(indexCell + 1),
                                          "{}_Image_{:02d}.tif".format(dt.strftime("%m_%d_%y_%Hh%Mm_%Ss"),
                                          indexImage + (numOfImages - 1) // 2 + 2)))
                cv2.imwrite(os.path.join(cwd, "FOV_{}".format(indexFov + 1), "Cell_{:03d}".format(indexCell + 1),
                                         "{}_Image_{:02d}.tif".format(dt.strftime("%m_%d_%y_%Hh%Mm_%Ss"),
                                         indexImage + (numOfImages - 1) // 2 + 2)), img)


if __name__ == '__main__':
    app.run(main)
