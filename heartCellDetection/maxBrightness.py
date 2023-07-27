import datetime
import os
import cv2
import numpy as np
from absl import app
from absl import flags
from absl import logging
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    r"C:\Victor\AIImageAnalysis\heartCellDetection\Dish1 50mW 2 cuts",
                    "Folder name")

# Define global variables
drawing = False
ix, iy = -1, -1
rect_endpoint_tmp = []

def plot_chart(image_path, output_directory):
    x = time_stamps

    y = [
        imageFile__.line_brightness
        for imageFile__ in imageFiles
    ]

    baseFolderName = os.path.basename(image_path)

    # save timeStamp, brightness result
    df = pd.DataFrame(x, columns=["Time"])
    df["signal"] = y

    csvFileName = baseFolderName + "_" + str(threshPercentage) + ".csv"
    csvFilePath = output_directory + '\\' + csvFileName
    print("csvFilePath: " + csvFilePath)

    df.to_csv(csvFilePath, index=False)
    
    title = os.path.basename(image_path)
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(x, y, "-o")
    plt.grid(True)
    locator = md.AutoDateLocator()
    formatter = md.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.ylabel("Brightness")
    plt.title(title)
    plt.tight_layout()

    baseFolderName = os.path.basename(image_path)
    chartFileName = baseFolderName + "_" + str(threshPercentage) + "_brightness_chart.png"
    chartFilePath = output_directory + '\\' + chartFileName
    print("chartFilePath: " + chartFilePath)
    plt.savefig(chartFilePath)

    # Display the plot
    plt.show()

def process_image_files(folder, laser_x1, laser_y1, laser_x2, laser_y2):
    file_names = os.listdir(folder)
    brightest_frame = None
    max_brightness = 0

    for file_name in file_names:
        if file_name.endswith(".tif"):
            file_path = os.path.join(folder, file_name)
            imageFile = ImageFile(file_name, file_path)
            imageFiles.append(imageFile)
            imageFile.laser_x1 = laser_x1
            imageFile.laser_y1 = laser_y1
            imageFile.laser_x2 = laser_x2
            imageFile.laser_y2 = laser_y2

            if file_name[2] == '_':
                year = int('20' + file_name[6:8])
                month = int(file_name[:2])
                day = int(file_name[3:5])
                hour = int(file_name[9:11])
                minute = int(file_name[12:14])
                second = int(file_name[16:18])
            elif file_name[3] == '_':
                year = int('20' + file_name[10:12])
                month = int(file_name[4:6])
                day = int(file_name[7:9])
                hour = int(file_name[13:15])
                minute = int(file_name[16:18])
                second = int(file_name[20:22])

            my_datetime = datetime.datetime(year, month, day, hour, minute, second)

            time_stamps.append(my_datetime)

            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            line_mask = np.zeros_like(img)
            cv2.line(line_mask, (laser_x1, laser_y1), (laser_x2, laser_y2), (65535, 65535, 65535), 3)
            line_pixels = img[line_mask == 65535]

            # Compute the average brightness of the line
            avg_brightness = np.mean(line_pixels)
            imageFile.line_brightness = avg_brightness

            normalized_img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            cv2.line(normalized_img, (laser_x1, laser_y1), (laser_x2, laser_y2), (0, 255, 0), 1)  # Line color is green, and line thickness is 2

            # if file_index == max_brightness_file_index:
            #     cv2.imshow("mask 2", normalized)
            #     cv2.waitKey(0)

            cv2.imshow("mask 2", normalized_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def find_brightest_frame_file(folder):
    file_names = os.listdir(folder)
    brightest_frame = None
    max_brightness = 0

    for file_name in file_names:
        if file_name.endswith(".tif"):
            file_path = os.path.join(folder, file_name)
            img = cv2.imread(file_path, -1)
            brightness = np.max(img)

            if brightness > max_brightness:
                max_brightness = brightness
                brightest_frame = file_path

    return brightest_frame

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, normalized_img, rect_endpoint_tmp

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        rect_endpoint_tmp = []

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = normalized_img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 1)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(normalized_img, (ix, iy), (x, y), (0, 255, 0), 1)
        rect_endpoint_tmp = [(ix, iy), (x, y)]

def find_farthest_points(contour):
    max_distance = 0
    farthest_pair = None

    for i in range(len(contour)):
        for j in range(i + 1, len(contour)):
            distance = cv2.norm(contour[i] - contour[j])

            if distance > max_distance:
                max_distance = distance
                farthest_pair = (contour[i], contour[j])

    return farthest_pair

class ImageFile:
    def __init__(self, fileName, filePath):
        self.fileName = fileName
        self.filePath = filePath
        self.laser_x1 = None
        self.laser_y1 = None
        self.laser_x2 = None
        self.laser_y2 = None
        self.line_brightness = None

def main(argv):
    global imageFiles
    imageFiles = []

    global time_stamps
    time_stamps = []
    global threshPercentage
    threshPercentage = 99

    global normalized_img
    folder_path = FLAGS.folder
    brightest_frame_file = find_brightest_frame_file(folder_path)

    if brightest_frame_file is not None:
        logging.info("Brightest frame: {}".format(brightest_frame_file))
        

        img = cv2.imread(brightest_frame_file, cv2.IMREAD_UNCHANGED)

        normalized_img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_rectangle)

        while True:
            cv2.imshow('image', normalized_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' to exit
                cv2.destroyAllWindows()
                break

        logging.info("Rectangle coordinates: {}".format(rect_endpoint_tmp))

        mask = np.zeros_like(img)
        mask[rect_endpoint_tmp[0][1]:rect_endpoint_tmp[1][1], rect_endpoint_tmp[0][0]:rect_endpoint_tmp[1][0]] = 65535
        masked_image = cv2.bitwise_and(img, mask)

        max_brightness = np.max(masked_image)
        print("The max brightness value in the image is: " + str(max_brightness))


        # max_brightness = np.max(masked_image)
        # print("The max brightness value in the image is: " + str(max_brightness))

        max_value_index = np.argmax(masked_image)
        max_brightness_y, max_brightness_x = np.unravel_index(max_value_index, img.shape)

        print("The brightest point is at (" + str(max_brightness_x) + ", " + str(max_brightness_y) + ")")

        normalized_masked_image = cv2.normalize(masked_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        height, width = normalized_img.shape

        # Calculate the area of the image
        image_area = height * width

        # Calculate the threshold value based on the 96% brightness level
        #thresh_val = np.percentile(normalized, 99.9)
        
        thresh_val = np.percentile(normalized_img, threshPercentage)

        # Apply the threshold to create a binary mask
        _, mask = cv2.threshold(normalized_img, thresh_val, 255, cv2.THRESH_BINARY_INV)

        # if file_index == max_brightness_file_index:
        #     cv2.imshow("mask", mask)
        #     cv2.waitKey(0)

        # 
        # Apply Canny edge detection
        edges = cv2.Canny(mask, 50, 150, apertureSize=3)

        contours, hierarchy = cv2.findContours(mask, cv2.
        RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour_index = None
        max_area = 0

        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            point = (float(max_brightness_x), float(max_brightness_y))  # Your point (x, y)

            result = cv2.pointPolygonTest(contour, point, False)

            #if result > 0 and area < image_area * .9:
            if result > 0:
                    contour_index = idx
        
        

        if (contour_index == None):
            print(brightest_frame_file + "has no contour dected!")

        else :

            # Draw contours on original image
            #cv2.drawContours(normalized, contours, contour_index = , (0, 0, 255), 2)
            
            farthest_points = find_farthest_points(contours[contour_index])

            pt1, pt2 = tuple(farthest_points[0][0]), tuple(farthest_points[1][0])
            cv2.line(normalized_img, pt1, pt2, (0, 255, 0), 1)  # Line color is green, and line thickness is 2

            # if file_index == max_brightness_file_index:
            #     cv2.imshow("mask 2", normalized)
            #     cv2.waitKey(0)

            cv2.imshow("mask 2", normalized_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Calculate the end points of the line
            x1 = pt1[0]
            y1 = pt1[1]
            x2 = pt2[0]
            y2 = pt2[1]
            
            img = cv2.imread(brightest_frame_file, cv2.IMREAD_UNCHANGED)
            line_mask = np.zeros_like(img)
            cv2.line(line_mask, (x1, y1), (x2, y2), (65535, 65535, 65535), 3)
            line_pixels = img[line_mask == 65535]

            # Compute the average brightness of the line
            avg_brightness = np.mean(line_pixels)

            max_avg_brightness = avg_brightness
            laser_x1 = x1
            laser_y1 = y1
            laser_x2 = x2
            laser_y2 = y2
            process_image_files(folder_path, laser_x1, laser_y1, laser_x2, laser_y2)

            output_directory = folder_path + '\\output'
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            plot_chart(folder_path, output_directory)
         

    else:
        logging.info("No frames found in the folder.")

if __name__ == "__main__":
    app.run(main)
