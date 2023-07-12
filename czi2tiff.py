import tifffile as tf
import numpy as np
import cv2
import os

input_czi = "D:\\UCI project Images\\9-24-19 Salsa Gsmtx4\\Cell 47 Pre.czi"
output_dir = "C:\\Users\\artho\\Pictures\\TestTiffs"
os.makedirs(output_dir, exist_ok=True)

print("Conversion successful, starting tif to tiff conversion", flush=True)

# Read the TIFF file
with tf.TiffFile(input_czi + ".tif") as tif:
    # Iterate over each timestamp
    for i, timestamp in enumerate(tif.pages):
        # Convert the timestamp to a separate TIFF file
        output_file = os.path.join(output_dir, f"{i}.tiff")
        tf.imwrite(output_file, timestamp.asarray())
        # grab newly created file
        src = cv2.imread(output_file)
        # extract green channel
        src[:,:,0]=0
        src[:,:,2]=0
        # overwrite initial image
        cv2.imwrite(output_file, src)

print("Conversion successful")
