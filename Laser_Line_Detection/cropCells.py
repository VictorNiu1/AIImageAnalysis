import cv2  
import tifffile as tiff
from cellpose import models, plot
import os
import glob
import matplotlib.pyplot as plt
from absl import app
from absl import logging
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('image_input_folder', r"C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\results\04112023 Tong KO 5787 5713\04112023 Tong KO 5787 5713\Dish2 KO 5787\FOV1 5 cells 50mW", 'Path to the folder containing the TIFF files')
flags.DEFINE_string('image_output_folder', r'C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\results\04112023 Tong KO 5787 5713\04112023 Tong KO 5787 5713\Dish2 KO 5787\FOV1 5 cells 50mW\output', 'Path to the folder where the output will be saved')
flags.DEFINE_integer('diameter', 120, 'Custom diameter value (in pixels) used for the cellpose model')

flags.mark_flag_as_required('image_input_folder')
flags.mark_flag_as_required('image_output_folder')

def get_tiff_files(image_input_folder):
    tiff_files = glob.glob(os.path.join(image_input_folder, '*.tiff'))
    tiff_files.extend(glob.glob(os.path.join(image_input_folder, '*.tif')))
    return tiff_files

def detect_cells(image, model):
    channels = [0, 0]
    diameter = FLAGS.diameter
    masks, _, _, _ = model.eval(image, diameter=diameter, channels=channels)
    return masks

def save_cropped_cells(image, masks, image_output_folder, image_path, prefix='cell'):
    num_cells = masks.max()

    for i in range(1, num_cells + 1):
        mask = masks == i
        ymin, xmin = mask.nonzero()[0].min(), mask.nonzero()[1].min()
        ymax, xmax = mask.nonzero()[0].max(), mask.nonzero()[1].max()

        cropped_cell = image[ymin:ymax+1, xmin:xmax+1]

        cell_image_output_folder = os.path.join(image_output_folder, f'{prefix}_{i}')
        if not os.path.exists(cell_image_output_folder):
            os.makedirs(cell_image_output_folder)

        image_name = os.path.splitext(os.path.basename(image_path))[0]
        tiff.imwrite(os.path.join(cell_image_output_folder, f'{image_name}.tiff'), cropped_cell)

        logging.info(f'Saved cropped cell {prefix}_{i} from {image_path}')

def draw_cell_indices(mask_overlay, masks):
    num_cells = masks.max()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 2

    for i in range(1, num_cells + 1):
        mask = masks == i
        y, x = mask.nonzero()[0].mean(), mask.nonzero()[1].mean()
        cv2.putText(mask_overlay, f"C_{str(i)}", (int(x), int(y)), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    return mask_overlay

def main(argv):
    image_input_folder = FLAGS.image_input_folder
    image_output_folder = FLAGS.image_output_folder

    image_paths = get_tiff_files(image_input_folder)
    logging.info(f'Found {len(image_paths)} TIFF files in {image_input_folder}')

    model = models.Cellpose(gpu=True, model_type='cyto')

    first_image_path = image_paths[0]
    first_image = tiff.imread(first_image_path)
    masks = detect_cells(first_image, model)

    image_rgb = cv2.cvtColor(first_image, cv2.COLOR_GRAY2RGB)

    mask_overlay = plot.mask_overlay(image_rgb, masks)

    mask_overlay_with_indices = draw_cell_indices(mask_overlay, masks)
    plt.imshow(mask_overlay_with_indices)
    plt.title('Cell Detection')
    plt.show()

    overlay_image_output_folder = os.path.join(image_output_folder, 'output')
    if not os.path.exists(overlay_image_output_folder):
        os.makedirs(overlay_image_output_folder)

    overlay_output_file = os.path.join(
        overlay_image_output_folder,
        f'{os.path.splitext(os.path.basename(first_image_path))[0]}_overlay.png',
    )
    cv2.imwrite(overlay_output_file, cv2.cvtColor(mask_overlay_with_indices, cv2.COLOR_RGB2BGR))

    for image_path in image_paths:
        image = tiff.imread(image_path)
        save_cropped_cells(image, masks, image_output_folder, image_path)

    logging.info('Cell detection and cropping completed.')

if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)
    app.run(main)