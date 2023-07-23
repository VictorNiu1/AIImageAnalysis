import os
import cv2
import numpy as np
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS
flags.DEFINE_string("folder",
                    r"C:\Users\Victor\Documents\GitHub\AIImageAnalysis\heartCellDetection\Heart Cell Project with Joe _ Bo\Heart Cell Project 12142022\Dish1 50mW 2 cuts",
                    "Folder name")

def find_brightest_frame(folder):
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

def main(argv):
    folder_name = FLAGS.folder
    brightest_frame = find_brightest_frame(folder_name)
    
    if brightest_frame is not None:
        logging.info("Brightest frame: {}".format(brightest_frame))
        
        # Load and display the brightest frame
        img = cv2.imread(brightest_frame, -1)
        normalized_img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cv2.imshow("Brightest Frame", normalized_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    else:
        logging.info("No frames found in the folder.")

if __name__ == "__main__":
    app.run(main)