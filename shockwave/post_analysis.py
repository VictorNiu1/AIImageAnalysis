import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from absl import app
from absl import flags
from absl import logging
import tools

FLAGS = flags.FLAGS
flags.DEFINE_string('folder',
                    r'C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4\output',
                    'Folder name')
flags.DEFINE_string('filename', r'final_brightness.csv', 'result name')
flags.DEFINE_float('threshold', r'1.1', 'threshold')


def main(argv):
    plt.rcParams['font.size'] = '14'
    style = 'seaborn-v0_8-darkgrid'
    plt.style.use(style)
    folderName = FLAGS.folder
    fileName = FLAGS.filename
    df = pd.read_csv(os.path.join(folderName, fileName))
    columns = df.columns
    logging.debug("columns are {}".format(columns))
    threshold = float(FLAGS.threshold)
    resultDf = pd.DataFrame()
    logging.info("{} Start image analysis {}".format(50 * "=", 50 * "="))
    for column in columns[2:]:
        logging.info(column)
        dataIn = np.array(df[column])
        baseline = df[column] - df['background']
        dataIn = baseline / baseline[0]

        energy, riseTime, fallTime, maxLoc, left, right = tools.timing_energy(dataIn, threshold=threshold)
        peakLocation, peakVal, fwhm, leftIdx, rightIdx = tools.full_width_half_maximum(dataIn)
        temp = pd.DataFrame()
        temp['roi'] = [column.split("_")[1]]
        temp['background'] = [df['background'].iloc[peakLocation]]
        temp['baseline'] = [baseline[0]]
        temp['threshold'] = [threshold]
        temp['peak'] = [peakVal]
        temp['peak_location'] = [peakLocation]
        temp['FWHM'] = [fwhm]
        temp['rise_time'] = [riseTime]
        temp['fall_time'] = [fallTime]
        temp['energy'] = [energy]
        temp['fwhm_left_index'] = [leftIdx]
        temp['fwhm_right_index'] = [rightIdx]
        temp['threshold_left_index'] = [left]
        temp['threshold_right_index'] = [right]
        resultDf = pd.concat([resultDf, temp])

        # generate graph
        plt.figure(figsize=(8, 6))
        plt.plot(dataIn, '-', lw=2)
        plt.plot(peakLocation, peakVal, 'h', markersize=12)
        plt.plot(leftIdx, peakVal / 2, 'cx', markersize=12)
        plt.plot(rightIdx, peakVal / 2, 'mx', markersize=12)
        plt.axhline(y=peakVal / 2, color='r', linestyle=':', lw=1.5)
        plt.axhline(y=threshold, color='g', linestyle='-.', lw=1.5)

        plt.axvline(x=leftIdx, color='r', linestyle=':', lw=1.5)
        plt.axvline(x=rightIdx, color='r', linestyle=':', lw=1.5)
        plt.axvline(x=left, color='b', linestyle=':', lw=1.5)
        plt.axvline(x=right, color='b', linestyle=':', lw=1.5)
        plt.text(leftIdx + 10, peakVal * .55, "FWHM is {:.3f}".format(fwhm))
        plt.text(left + 10, threshold + .1, "Rise time is {:.3f}".format(riseTime))
        plt.text(len(dataIn) // 2, threshold + .1, "Fall time is {:.3f}".format(fallTime))
        plt.title("{}".format(column))
        plt.xlabel("Frame Index")
        plt.ylabel("Signal [DN]")
        plt.tight_layout()
        plt.savefig(os.path.join(folderName, "statistics_{}.png".format(column)), dpi=150)
        plt.close()
    resultDf.to_csv(os.path.join(folderName, "statistics.csv"), index=False)
    logging.info("{} Finish image analysis {}".format(49 * "=", 49 * "="))
    plt.show()


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    app.run(main)
