import datetime
import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

#background_x1, background_y1, background_x2, background_y2 = 310, 139, 426, 269
# Define the length of the line
line_length = 45
#line_length = 30

# Specify the directory containing the files
directory = 'Images after laser cutting for AI project/1 DNA repair/U2OS_53KO_5979GFP_FOV3'
#directory = 'Images after laser cutting for AI project\\1 DNA repair\\U2OS_WT_5979GFP_FOV2'
#directory = 'Images after laser cutting for AI project\\1 DNA repair\\U2OS_WT_5979GFP_FOV3'
#directory = 'Images after laser cutting for AI project\\1 DNA repair\\09182021\\09182021 SETX KO 1A5'
#directory = 'Images after laser cutting for AI project\\1 DNA repair\\04112011 images'

# The code reads a set of TIFF image files from a specified directory and stores them in an array. 
# It also stores the maximum pixel brightness value and its location in each image file model. 
# It then goes through each image file and rotates a line of specified length around the maximum pixel brightness location 
# to a specified degree increment (1 degree a time to rotate). 
# The code calculates the average brightness of each line and finds the angle of rotation where the line has the maximum average brightness.
# Finally, it plots a chart of x axis of time span in seconds and y axis of the average brightness of the cut line
def main():
    # Get a list of all files in the directory with a ".tif" extension
    file_list = [f for f in os.listdir(directory) if f.endswith('.tif')]

    # Sort the file list alphabetically
    file_list.sort()

    imageFiles = []

    # Create an array of time differences in seconds for Y axis
    time_diffs = []

    max_brightness_file_index = find_max_brightness_file(file_list, imageFiles, time_diffs)

    populate_imagefiles_model(imageFiles)

    reset_cut_line_for_all_files(imageFiles, max_brightness_file_index)

    #press any key to show next normailized image with the cut line
    draw_line_and_show(imageFiles)

    plot_chart(imageFiles, time_diffs)


def plot_chart(imageFiles, time_diffs):
    x = time_diffs

    y = [
        imageFile__.max_avg_brightness - imageFile__.backgroudPointbrightness
        for imageFile__ in imageFiles
    ]
    # Create the plot
    plt.plot(x, y)

    # Add labels and title
    plt.xlabel('X-axis: seconds')
    plt.ylabel('Y-axis: mean(brightness)')
    plt.title('My plot')

    # Display the plot
    plt.show()

def draw_line_and_show(imageFiles):
    for imageFile in imageFiles:
        img = cv2.imread(imageFile.filePath, cv2.IMREAD_UNCHANGED)

        #img = cv2.imread('09_06_22_14h09m_10s_ms024__E03U2OS_53KO_5979GFP.tif', cv2.IMREAD_UNCHANGED)
        # Normalize pixel values to 0-255 range
        normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        theta = math.radians(imageFile.angle_of_max_brightness)
        x1 = int(imageFile.max_brightness_x - line_length / 2 * math.cos(theta))
        y1 = int(imageFile.max_brightness_y - line_length / 2 * math.sin(theta))
        x2 = int(imageFile.max_brightness_x + line_length / 2 * math.cos(theta))
        y2 = int(imageFile.max_brightness_y + line_length / 2 * math.sin(theta))
        line = cv2.line(normalized, (x1, y1), (x2, y2), 0,1)

        # Show the image with the rectangle
        cv2.imshow('Brightest Pixel', normalized)
        cv2.waitKey(0)

def reset_cut_line_for_all_files(imageFiles, max_brightness_file_index):
    for file_index in range(len(imageFiles)):
        if (max_brightness_file_index != file_index):
            img = cv2.imread(imageFiles[file_index].filePath, cv2.IMREAD_UNCHANGED)

            #normalized = cv2.normalize(img, None, 0, 65535, cv2.NORM_MINMAX, cv2.CV_16U)
            normalized = img
            # Define the center point of the line
            x = imageFiles[max_brightness_file_index].max_brightness_x
            y = imageFiles[max_brightness_file_index].max_brightness_y

            # Define the angle of rotation in degrees
            angle_radians = math.radians(imageFiles[max_brightness_file_index].angle_of_max_brightness)

            # Calculate the end points of the line
            x1 = int(imageFiles[max_brightness_file_index].max_brightness_x - (line_length / 2) * math.cos(angle_radians))
            y1 = int(imageFiles[max_brightness_file_index].max_brightness_y - (line_length / 2) * math.sin(angle_radians))
            x2 = int(imageFiles[max_brightness_file_index].max_brightness_x + (line_length / 2) * math.cos(angle_radians))
            y2 = int(imageFiles[max_brightness_file_index].max_brightness_y + (line_length / 2) * math.sin(angle_radians))

            line_mask = np.zeros_like(normalized)
            cv2.line(line_mask, (x1, y1), (x2, y2), (65535, 65535, 65535), 6)
            line_pixels = normalized[line_mask == 65535]

            # Compute the average brightness of the line
            avg_brightness = np.mean(line_pixels)
            imageFiles[file_index].max_avg_brightness = avg_brightness
            imageFiles[file_index].angle_of_max_brightness = imageFiles[max_brightness_file_index].angle_of_max_brightness
            imageFiles[file_index].max_brightness_x = imageFiles[max_brightness_file_index].max_brightness_x
            imageFiles[file_index].max_brightness_y = imageFiles[max_brightness_file_index].max_brightness_y
  
def populate_imagefiles_model(imageFiles):
    for imageFile in imageFiles:
        file_path = imageFile.filePath
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        # Define the center point of the line
        x, y = imageFile.max_brightness_x, imageFile.max_brightness_y

        # Define the angle of rotation in degrees
        max_avg_brightness = 0
        angle_of_max_brightness = 0

        for angle_degrees in range(360):
            # Convert the angle to radians
                angle_radians = math.radians(angle_degrees)

                # Calculate the end points of the line
                x1 = int(x - (line_length / 2) * math.cos(angle_radians))
                y1 = int(y - (line_length / 2) * math.sin(angle_radians))
                x2 = int(x + (line_length / 2) * math.cos(angle_radians))
                y2 = int(y + (line_length / 2) * math.sin(angle_radians))

                line_mask = np.zeros_like(img)
                cv2.line(line_mask, (x1, y1), (x2, y2), (65535, 65535, 65535), 6)
                line_pixels = img[line_mask == 65535]

                # Compute the average brightness of the line
                avg_brightness = np.mean(line_pixels)

                print(f'avg_brightnessis is {avg_brightness}, angle is {angle_degrees}')
                if avg_brightness > max_avg_brightness:
                    max_avg_brightness = avg_brightness
                    angle_of_max_brightness = angle_degrees

        imageFile.max_avg_brightness = max_avg_brightness
        imageFile.angle_of_max_brightness = angle_of_max_brightness

        # # Extract the pixel values of the rectangular region
        # region = img[background_y1:background_y2, background_x1:background_x2]

        # # Compute the mean brightness of the pixels in the region
        #imageFile.backgroudPointbrightness = np.mean(region)
        imageFile.backgroudPointbrightness = 0

def find_max_brightness_file(file_list, imageFiles, time_diffs):
    max_brightness = 0
    max_brightness_file_index = 0

    for i, file_name in enumerate(file_list):
        file_path = os.path.join(directory, file_name)
        imageFile = ImageFile(file_name, file_path)
        imageFiles.append(imageFile)
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        # Find the pixel with the maximum value in the image
        max_value_index = np.argmax(img)
        imageFile.max_brightness = img.flat[max_value_index]

        if i > 0 and imageFile.max_brightness > max_brightness:
            max_brightness = imageFile.max_brightness
            max_brightness_file_index = i

        # Convert the flattened index back to row and column coordinates
        max_row, max_col = np.unravel_index(max_value_index, img.shape)
        imageFile.max_brightness_x, imageFile.max_brightness_y = max_col, max_row

        # Convert file name to datetime object
        year = int(file_name[6:8])
        month = int(file_name[:2])
        day = int(file_name[3:5])
        hour = int(file_name[9:11])
        minute = int(file_name[12:14])
        second = int(file_name[16:18])
        my_datetime = datetime.datetime(year, month, day, hour, minute, second)

        if i == 0:
            # Set the reference time to the time of the first file
            ref_time = my_datetime
            time_diffs.append(0.0)
        else:
            # Calculate the time difference in seconds between the current file and the reference time
            current_time = my_datetime
            time_diff = (current_time - ref_time).total_seconds()
            time_diffs.append(time_diff)

    return max_brightness_file_index

class ImageFile:
    def __init__(self, fileName, filePath):
        self.fileName = fileName
        self.filePath = filePath
        self.max_brightness = None
        self.max_brightness_x = None
        self.max_brightness_y = None

main()