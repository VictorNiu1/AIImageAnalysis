import os
import numpy as np
import matplotlib.pyplot as plt
import cv2


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
    plt.savefig("{}_overlay.png".format(filename[:-4]), dpi=150)
    plt.close()


def cell_detection(img: np.ndarray, gaussianKernal: tuple = (3, 3), imgMin: int = 0, imgMax: int = 255, boxX=30,
                   boxY=30):
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
    result = np.zeros((100, 4))
    for contour in contours:
        # Obtain the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # if w > boxX or h > boxY:
        if w > boxX and h > boxY:
            result[count, 0:6] = np.array([x, y, w, h])
            count += 1
    return np.uint16(result[:count - 1, :])


def main():
    folder = r"C:\Users\changfan\Downloads\1 DNA repair-20230319T175246Z-001\1 DNA repair\09182021\09182021\09182021 SETX KO WT"
    imageFiles = sorted([x for x in os.listdir(folder) if x.endswith("tif")])
    defaultRois = np.zeros((1, 1))
    for idx, imageFile in enumerate(imageFiles[:]):
        print(imageFile)

        # Read tiff image
        temp = cv2.imread(os.path.join(folder, imageFile), cv2.IMREAD_UNCHANGED)

        # Normalize pixel values to 0-255 range
        img = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        # roi detection
        rois = cell_detection(img)
        # np.savetxt("{}.csv".format(imageFile[:-4]), rois, delimiter=',', header="x,y,w,h")

        # display image
        # overlay_plot(temp, result, imageFile)

        if len(rois) > len(defaultRois):
            defaultRois = rois
    np.savetxt("ROIs.csv", defaultRois, delimiter=',', header="x,y,w,h", comment="")

    for idx, imageFile in enumerate(imageFiles[:]):
        temp = cv2.imread(os.path.join(folder, imageFile), cv2.IMREAD_UNCHANGED)
        for idy, roi in enumerate(defaultRois):
            # create roi folder
            if not os.path.exists(os.path.join(folder, "cell_{}".format(idy + 1))):
                os.makedirs(os.path.join(folder, "cell_{}".format(idy + 1)))

            x, y, w, h = roi
            cropImg = temp[y: y + h, x:x + w]
            cv2.imwrite(os.path.join(folder, "cell_{}".format(idy + 1), "{}_cell_{}.tiff".format(imageFile[:-4], idy)),
                        cropImg)


if __name__ == "__main__":
    main()
