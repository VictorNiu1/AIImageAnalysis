import datetime
import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
from absl import flags, app
import glob
# how to run in 
# (UCSDAIProject) C:\Victor\AIImageAnalysis>python C:\Victor\AIImageAnalysis\opencv\main.py --exclusion_x=0 --exclusion_y=91 --exclusion_width=26 --exclusion_height=26 --threshPercentage=97 --imageDirectory="C:\\Victor\\AIImageAnalysis\\Images after laser cutting for AI project\\1 DNA repair\\09182021\\09182021 SETX KO 1A5\\cell_16"

FLAGS = flags.FLAGS

flags.DEFINE_string("imageDirectory",
                     r"C:\Users\Victor\Documents\GitHub\AIImageAnalysis\heartCellDetection\testing",
                      "Single DNA folder")

flags.DEFINE_string("referenceImage",
                     r"C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\FOV6 4_17_40_PM 75mW cell shrink 1 min after cut\06_13_23_16h17m_56s_ms872__F8.tif",
                      "Single DNA folder")


flags.DEFINE_float('threshPercentage', 96, 'ThreshPercentage')
flags.DEFINE_float('slopeDifference',  30, 'slopeDifference')
flags.DEFINE_float('threshDistanceOfMaxBrightnessPoints', 30, 'ThreshDistanceOfMaxBrightnessPoints')



flags.DEFINE_integer('exclusion_x', 0, 'exclusion x')
flags.DEFINE_integer('exclusion_y', 0, 'exclusion y')
flags.DEFINE_integer('exclusion_width', 0, 'exclusion width')
flags.DEFINE_integer('exclusion_height', 0, 'exclusion height')


#flags.DEFINE_integer('exclusion_x', 62, 'exclusion x')
#flags.DEFINE_integer('exclusion_y', 62, 'exclusion y')
#flags.DEFINE_integer('exclusion_width', 60, 'exclusion width')
#flags.DEFINE_integer('exclusion_height', 60, 'exclusion height')


image_directory = ""
output_directory = ""


def main(argv):
    global reference_Image
    reference_Image = FLAGS.referenceImage

    global image_directory
    image_directory = FLAGS.imageDirectory

    print("FLAGS.imageDirectory: " + FLAGS.imageDirectory)
    global slopeDifference
    slopeDifference = FLAGS.slopeDifference

    global threshPercentage
    threshPercentage = FLAGS.threshPercentage

    global threshDistanceOfMaxBrightnessPoints
    threshDistanceOfMaxBrightnessPoints = FLAGS.threshDistanceOfMaxBrightnessPoints

    global output_directory
    output_directory = image_directory + '\\output'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    # Access flag values
    print('exclusion width:', FLAGS.exclusion_width)
    

    # Get a list of all files in the directory with a ".tif" extension
    file_list = [f for f in os.listdir(image_directory) if (f.endswith('.tif') or f.endswith('.tiff'))]

    # Sort the file list alphabetically
    file_list.sort()

    imageFiles = []

    # Create an array of time differences in seconds for Y axis
    time_stamps = []

    imageFiles, time_stamps, max_brightness_file_index = build_imagefile_models(file_list, imageFiles, time_stamps)
    
    find_laser_line(imageFiles, max_brightness_file_index)

    reset_cut_line_for_all_files(imageFiles, max_brightness_file_index)

    #press any key to show next normailized image with the cut line
    draw_line_and_show(imageFiles)

    plot_chart(imageFiles, time_stamps)

def build_imagefile_models(file_list, imageFiles, time_stamps):
    max_brightness_file_index = find_max_brightness_file(file_list, imageFiles, time_stamps)
    print(f"max_brightness_file_index: {str(max_brightness_file_index)}")
    print("max_brightness_file: " + imageFiles[max_brightness_file_index].filePath)

    # (x, y) coordinates of the center
    center = (imageFiles[max_brightness_file_index].max_brightness_x, imageFiles[max_brightness_file_index].max_brightness_y)  
    side_length = 10

    mean_values = calculate_mean_values(imageFiles, center, side_length)
    standard_deviation = np.std(mean_values)
    mean_value = np.mean(mean_values)

    print(mean_values)
    print("standard_deviation:" + str(standard_deviation))
    print("standard_deviation/mean_value:" + str(standard_deviation/mean_value))

    # if(standard_deviation/mean_value < .05):
    #     FLAGS.exclusion_x = int(imageFiles[max_brightness_file_index].max_brightness_x - side_length / 2)
    #     FLAGS.exclusion_y = int(imageFiles[max_brightness_file_index].max_brightness_y - side_length / 2)
    #     FLAGS.exclusion_width = side_length
    #     FLAGS.exclusion_height = side_length
    #     imageFiles = []  
    #     time_stamps = []
    #     max_brightness_file_index = find_max_brightness_file(file_list, imageFiles, time_stamps)
    return imageFiles,time_stamps,max_brightness_file_index

def get_tiff_files(folder_path):
    tiff_files = glob.glob(os.path.join(folder_path, '*.tiff'))
    tiff_files.extend(glob.glob(os.path.join(folder_path, '*.tif')))
    return tiff_files

def get_square_coordinates(center, side_length):
    half_side = side_length // 2
    top_left = (center[0] - half_side, center[1] - half_side)
    bottom_right = (center[0] + half_side, center[1] + half_side)
    return top_left, bottom_right

def mean_value_in_square(image, center, side_length):
    top_left, bottom_right = get_square_coordinates(center, side_length)
    square_image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return square_image.mean()

def calculate_mean_values(imageFiles, center, side_length):
    mean_values = []
    for file_index in range(len(imageFiles)):
        imageFile = imageFiles[file_index]
        img = cv2.imread(imageFile.filePath, cv2.IMREAD_UNCHANGED)
        mean_value = mean_value_in_square(img, center, side_length)
        mean_values.append(mean_value)
    return mean_values

def plot_chart(imageFiles, time_stamps):
    x = time_stamps

    y = [
        imageFile__.max_avg_brightness - imageFile__.backgroudPointbrightness
        for imageFile__ in imageFiles
    ]

    baseFolderName = os.path.basename(image_directory)

    # save timeStamp, brightness result
    df = pd.DataFrame(x, columns=["Time"])
    df["signal"] = y

    csvFileName = baseFolderName + "_" + str(threshPercentage) + ".csv"
    csvFilePath = output_directory + '\\' + csvFileName
    print("csvFilePath: " + csvFilePath)

    df.to_csv(csvFilePath, index=False)
    
    title = os.path.basename(FLAGS.imageDirectory)
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

    baseFolderName = os.path.basename(image_directory)
    chartFileName = baseFolderName + "_" + str(threshPercentage) + "_brightness_chart.png"
    chartFilePath = output_directory + '\\' + chartFileName
    print("chartFilePath: " + chartFilePath)
    plt.savefig(chartFilePath)

    # Display the plot
    plt.show()


def draw_line_and_show(imageFiles):
    # setup 4 subplot on each row
    cols = 3
    rows = int(np.ceil(len(imageFiles) / cols))
    plt.rcParams['font.size'] = '6'
    style = 'seaborn-v0_8-darkgrid'
    plt.style.use(style)
    plt.figure(figsize=(12, 12))
    for file_index in range(len(imageFiles)):
        imageFile = imageFiles[file_index]
        img = cv2.imread(imageFile.filePath, cv2.IMREAD_UNCHANGED)

        # Normalize pixel values to 0-255 range
        normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        line = cv2.line(normalized, (imageFile.laser_x1, imageFile.laser_y1), (imageFile.laser_x2, imageFile.laser_y2), 0, 1)
            
        center_x = (imageFile.laser_x1 + imageFile.laser_x2) / 2
        center_y = (imageFile.laser_y1 + imageFile.laser_y2) / 2

        width = 120
        height = 120
        # Calculate the starting and ending points of the crop
        start_x = int(center_x - (width / 2))
        end_x = int(center_x + (width / 2))
        start_y = int(center_y - (height / 2))
        end_y = int(center_y + (height / 2))

        # Crop the image
        if (start_x > 0 and start_y > 0):
            cropped_img = normalized[start_y:end_y, start_x:end_x]
        else:
            cropped_img = normalized

        plt.subplot(rows, cols, file_index + 1)
        
        plt.imshow(cropped_img, cmap="gray")

        plt.title(os.path.splitext(imageFile.fileName)[0])
        plt.grid(False)
        plt.tight_layout()
    
    baseFolderName = os.path.basename(image_directory)
    pngFileName = baseFolderName + "_" + str(threshPercentage) + ".png"
    pngFilePath = output_directory + '\\' + pngFileName
    print("pngFilePath: " + pngFilePath)
    plt.savefig(pngFilePath)

def calculate_slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1) if x1 != x2 else float('inf')

def is_similiar_slope(slope1, slope2, threshold_percent):
    # Calculate the relative difference between the slopes
    difference = abs(slope1 - slope2)
    average = (abs(slope1) + abs(slope2)) / 2
    relative_difference = difference / average

    print(f'relative_difference:{str(relative_difference)}')
    # Check if the relative difference is less than the threshold
    return relative_difference <= threshold_percent / 100

def reset_cut_line_for_all_files(imageFiles, max_brightness_file_index):
    base_file_max_brightness_x = imageFiles[max_brightness_file_index].max_brightness_x
    base_file_max_brightness_y = imageFiles[max_brightness_file_index].max_brightness_y
    max_brightness_line_slope = calculate_slope(imageFiles[max_brightness_file_index].laser_x1, imageFiles[max_brightness_file_index].laser_y1, imageFiles[max_brightness_file_index].laser_x2, imageFiles[max_brightness_file_index].laser_y2)
    for file_index in range(len(imageFiles)):
        if (file_index == max_brightness_file_index):
            continue

        max_brightness_x = imageFiles[file_index].max_brightness_x
        max_brightness_y = imageFiles[file_index].max_brightness_y
        if (hasattr(imageFiles[file_index], "laser_x1") == False):
            imageFiles[file_index].laser_x1 = 0
            imageFiles[file_index].laser_y1 = 0
            imageFiles[file_index].laser_x2 = 0
            imageFiles[file_index].laser_y2 = 0

        currentLineSlope = calculate_slope(imageFiles[file_index].laser_x1, imageFiles[file_index].laser_y1, imageFiles[file_index].laser_x2, imageFiles[file_index].laser_y2)

        point1 = np.array([base_file_max_brightness_x, base_file_max_brightness_y])
        point2 = np.array([max_brightness_x, max_brightness_y])
        # Differences of slopes
        distance = np.linalg.norm(point2 - point1)
        isSimiliarSlope = is_similiar_slope(currentLineSlope, max_brightness_line_slope, slopeDifference)

        
        print(f'isSimiliarSlope:{str(isSimiliarSlope)}')

        if (distance > threshDistanceOfMaxBrightnessPoints or isSimiliarSlope == False):
            img = cv2.imread(imageFiles[file_index].filePath, cv2.IMREAD_UNCHANGED)

            #normalized = cv2.normalize(img, None, 0, 65535, cv2.NORM_MINMAX, cv2.CV_16U)
            normalized = img
            # Define the center point of the line
            x = imageFiles[max_brightness_file_index].max_brightness_x
            y = imageFiles[max_brightness_file_index].max_brightness_y

            line_mask = np.zeros_like(normalized)
            cv2.line(line_mask, (imageFiles[max_brightness_file_index].laser_x1, imageFiles[max_brightness_file_index].laser_y1), (imageFiles[max_brightness_file_index].laser_x2, imageFiles[max_brightness_file_index].laser_y2), (65535, 65535, 65535), 6)
            line_pixels = normalized[line_mask == 65535]

            # Compute the average brightness of the line
            avg_brightness = np.mean(line_pixels)
            imageFiles[file_index].max_avg_brightness = avg_brightness
            #imageFiles[file_index].angle_of_max_brightness = imageFiles[max_brightness_file_index].angle_of_max_brightness
            imageFiles[file_index].max_brightness_x = imageFiles[max_brightness_file_index].max_brightness_x
            imageFiles[file_index].max_brightness_y = imageFiles[max_brightness_file_index].max_brightness_y
            imageFiles[file_index].laser_x1 = imageFiles[max_brightness_file_index].laser_x1
            imageFiles[file_index].laser_y1 = imageFiles[max_brightness_file_index].laser_y1
            imageFiles[file_index].laser_x2 = imageFiles[max_brightness_file_index].laser_x2
            imageFiles[file_index].laser_y2 = imageFiles[max_brightness_file_index].laser_y2

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

def find_laser_line(imageFiles, max_brightness_file_index):
    for file_index in range(len(imageFiles)):
        imageFile = imageFiles[file_index]
        # Read tiff image
        file_path = imageFile.filePath
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        height, width = normalized.shape

        # Calculate the area of the image
        image_area = height * width

        # Calculate the threshold value based on the 96% brightness level
        #thresh_val = np.percentile(normalized, 99.9)
        thresh_val = np.percentile(normalized, threshPercentage)

        # Apply the threshold to create a binary mask
        _, mask = cv2.threshold(normalized, thresh_val, 255, cv2.THRESH_BINARY_INV)

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
            point = (float(imageFile.max_brightness_x), float(imageFile.max_brightness_y))  # Your point (x, y)

            result = cv2.pointPolygonTest(contour, point, False)

            if result > 0 and area < image_area * .9:
                    contour_index = idx
        
        

        if (contour_index == None):
            print(imageFile.filePath + "has no contour dected!")
            print("the brigtest point is at (" + str(imageFile.max_brightness_x) + ", " + str(imageFile.max_brightness_y) + ")")
            continue

        # Draw contours on original image
        #cv2.drawContours(normalized, contours, contour_index = , (0, 0, 255), 2)
        
        farthest_points = find_farthest_points(contours[contour_index])

        pt1, pt2 = tuple(farthest_points[0][0]), tuple(farthest_points[1][0])
        cv2.line(normalized, pt1, pt2, (0, 255, 0), 2)  # Line color is green, and line thickness is 2

        # if file_index == max_brightness_file_index:
        #     cv2.imshow("mask 2", normalized)
        #     cv2.waitKey(0)

        cv2.imshow("mask 2", normalized)
        cv2.waitKey(0)


        # Calculate the end points of the line
        x1 = pt1[0]
        y1 = pt1[1]
        x2 = pt2[0]
        y2 = pt2[1]
        
        img = cv2.imread(imageFile.filePath, cv2.IMREAD_UNCHANGED)
        line_mask = np.zeros_like(img)
        cv2.line(line_mask, (x1, y1), (x2, y2), (65535, 65535, 65535), 6)
        line_pixels = img[line_mask == 65535]

        # Compute the average brightness of the line
        avg_brightness = np.mean(line_pixels)

        imageFile.max_avg_brightness = avg_brightness
        imageFile.laser_x1 = x1
        imageFile.laser_y1 = y1
        imageFile.laser_x2 = x2
        imageFile.laser_y2 = y2
    
    if (hasattr(imageFiles[max_brightness_file_index], "laser_x1") == False):
        detectedImageFile = None
        for i in range(len(imageFiles) - 1, -1, -1):
            if hasattr(imageFiles[i], "laser_x1"):
                detectedImageFile = imageFiles[i]
                break                
        
        imageFiles[max_brightness_file_index].laser_x1 = detectedImageFile.laser_x1
        imageFiles[max_brightness_file_index].laser_y1 = detectedImageFile.laser_y1
        imageFiles[max_brightness_file_index].laser_x2 = detectedImageFile.laser_x2
        imageFiles[max_brightness_file_index].laser_y2 = detectedImageFile.laser_y2

        img = cv2.imread(imageFiles[max_brightness_file_index].filePath, cv2.IMREAD_UNCHANGED)
        line_mask = np.zeros_like(img)
        cv2.line(line_mask, (imageFiles[max_brightness_file_index].laser_x1, imageFiles[max_brightness_file_index].laser_y1), (imageFiles[max_brightness_file_index].laser_x2, imageFiles[max_brightness_file_index].laser_y2), (65535, 65535, 65535), 6)
        line_pixels = img[line_mask == 65535]

        # Compute the average brightness of the line
        avg_brightness = np.mean(line_pixels)

        imageFiles[max_brightness_file_index].max_avg_brightness = avg_brightness



        

def find_max_brightness_file(file_list, imageFiles, time_stamps):
    max_brightness = 0
    max_brightness_file_index = 0
    for i, file_name in enumerate(file_list):
        file_path = os.path.join(image_directory, file_name)
        imageFile = ImageFile(file_name, file_path)
        imageFiles.append(imageFile)
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        # Create a copy of the image to exclude the rectangular region
        if FLAGS.exclusion_x == 0 and FLAGS.exclusion_y == 0 and FLAGS.exclusion_width == 0 and FLAGS.exclusion_height == 0:
            img_excluded = img
        else:
            img_excluded = np.copy(img)
            img_excluded[FLAGS.exclusion_y:FLAGS.exclusion_y + FLAGS.exclusion_height, FLAGS.exclusion_x:FLAGS.exclusion_x + FLAGS.exclusion_width] = 0
            
        
        # Find the pixel with the maximum value in the image

        max_value_index = np.argmax(img_excluded)
        imageFile.max_brightness = img_excluded.flat[max_value_index]

        #imageFile.backgroudPointbrightness = np.mean(img)
        imageFile.backgroudPointbrightness = 0

        if i > 0 and imageFile.max_brightness > max_brightness:
            max_brightness = imageFile.max_brightness
            max_brightness_file_index = i

        # Convert the flattened index back to row and column coordinates
        max_row, max_col = np.unravel_index(max_value_index, img.shape)
        imageFile.max_brightness_x, imageFile.max_brightness_y = max_col, max_row

        # Convert file name to datetime object
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

    return max_brightness_file_index

class ImageFile:
    def __init__(self, fileName, filePath):
        self.fileName = fileName
        self.filePath = filePath
        self.max_brightness = None
        self.max_brightness_x = None
        self.max_brightness_y = None

if __name__ == "__main__":
    app.run(main)