# Crop Cells Instruction
Python script to cropt multiple cells in order to run the Line Detection Algorithm.
## Get help
Go to Anaconda Navigator and launch Terminal. Navigate to the file Laser_Line_Detection. 

Example: cd C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection

Type: python cropCells.py --help 

result:
cropCells.py:16: UserWarning: Flag --image_input_folder has a non-None default value; therefore, mark_flag_as_required will pass even if flag is not specified in the command line!
  flags.mark_flag_as_required('image_input_folder')
cropCells.py:17: UserWarning: Flag --image_output_folder has a non-None default value; therefore, mark_flag_as_required will pass even if flag is not specified in the command line!
  flags.mark_flag_as_required('image_output_folder')


       USAGE: cropCells.py [flags]
flags:

cropCells.py:
  --diameter: Custom diameter value (in pixels) used for the cellpose model
    (default: '120')
    (an integer)
  --image_input_folder: Path to the folder containing the TIFF files
    (default:
    'C:\\Users\\hongy\\OneDrive\\Documents\\GitHub\\AIImageAnalysis\\Images
    after laser cutting for AI project\\1 DNA repair\\04112023 Tong KO 5787
    5713\\04112023 Tong KO 5787 5713\\Dish1 KO 5713\\FOV4 6 cells 50mW')
  --image_output_folder: Path to the folder where the output will be saved
    (default: 'C:\\temp\\8')

Try --helpfull to get a list of all flags.


                                                        
## Example on how to run the crop cells                                                                        
python cropCells.py --image_input_folder="C:\Victor\AIImageAnalysis\Images after laser cutting for AI project\1 DNA repair\04122023 Tong WT 5713 5787\04122023 Tong WT 5713 5787\Dish1 WT 5713 50 mW\FOV2 10 cells 4 lines" --image_output_folder="C:\Victor\AIImageAnalysis\Images after laser cutting for AI project\1 DNA repair\04122023 Tong WT 5713 5787\04122023 Tong WT 5713 5787\Dish1 WT 5713 50 mW\FOV2 10 cells 4 lines\output" --diameter=100       

## result
PS C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis>  c:; cd 'c:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis'; & 'C:\Users\hongy\anaconda3\envs\UCSDAIProject\python.exe' 'c:\Users\hongy\.vscode\extensions\ms-python.python-2023.8.0\pythonFiles\lib\python\debugpy\adapter/../..\debugpy\launcher' '62225' '--' 'c:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\cropCells.py'
c:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\cropCells.py:16: UserWarning: Flag --image_input_folder has a non-None default value; therefore, mark_flag_as_required will pass even if flag is not specified in the command line!
  flags.mark_flag_as_required('image_input_folder')
c:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\cropCells.py:17: UserWarning: Flag --image_output_folder has a non-None default value; therefore, mark_flag_as_required will pass even if flag is not specified in the command line!
  flags.mark_flag_as_required('image_output_folder')
I0528 19:04:08.108587  1224 core.py:62] TORCH CUDA version not installed/working.
I0528 19:04:08.108587  1224 core.py:90] >>>> using CPU
I0528 19:04:08.109588  1224 models.py:338] >> cyto << model set to be used
I0528 19:04:08.206756  1224 models.py:372] >>>> model diam_mean =  30.000 (ROIs rescaled to this size during training)
I0528 19:04:08.208746  1224 models.py:238] ~~~ FINDING MASKS ~~~
I0528 19:04:10.119260  1224 models.py:262] >>>> TOTAL TIME 1.91 sec

# Single Cell Detection  Instruction
Python script to cropt multiple cells in order to run the Line Detection Algorithm.
## Get help
Go to Anaconda Navigator and launch Terminal. Navigate to the file Laser_Line_Detection. 

Example: cd C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection

Type: python singleCellDetection.py --help 

result:

       USAGE: cropCells.py [flags]
flags:

singleCellDetection.py:
  --exclusion_height: exclusion height
    (default: '0')
    (an integer)
  --exclusion_width: exclusion width
    (default: '0')
    (an integer)
  --exclusion_x: exclusion x
    (default: '0')
    (an integer)
  --exclusion_y: exclusion y
    (default: '0')
    (an integer)
  --imageDirectory: Single DNA folder
    (default: 'C:\\Users\\hongy\\OneDrive\\Documents\\GitHub\\AIImageAnalysis\\L
    aser_Line_Detection\\sample_result\\output\\cell_7')
  --threshDistanceOfMaxBrightnessPoints: ThreshDistanceOfMaxBrightnessPoints
    (default: '30.0')
    (a number)
  --threshPercentage: ThreshPercentage
    (default: '85.0')
    (a number)

Try --helpfull to get a list of all flags.

                                                        
## Example on how to run the crop cells                                                                        
python singleCellDetection.py --exclusion_height=0 -- exclusion_width=0 -- exclusion_x=0 -- exclusion_y =0 --imageDirectory="C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\sample_result\output\cell_7"--threshDistanceOfMaxBrightnessPoints= 30.0 -- threshPercentage 85.0

## result
FLAGS.imageDirectory: C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\sample_result\output\cell_7
exclusion width: 0
max_brightness_file_index: 7
max_brightness_file: C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\sample_result\output\cell_7\09_18_21_12h44m_37s_ms018__E07U2OS_SETX_KO_1A4.tiff
[1298.2, 1487.7, 1579.9, 1580.66, 1583.97, 1581.57, 1581.38, 1581.33, 1578.49, 1577.41, 1572.2, 1568.84, 1569.39, 1569.45, 1568.67, 1566.4, 1565.55, 1563.26, 1563.87, 1561.79, 1561.04, 1558.64, 1558.92]
standard_deviation:57.981925010966265
standard_deviation/mean_value:0.03727320680675097
relative_difference:0.6408768536428111
isSimiliarSlope:False
relative_difference:2.0
isSimiliarSlope:False
relative_difference:0.8603351955307262
isSimiliarSlope:False
relative_difference:0.01261523532265885
isSimiliarSlope:True
relative_difference:0.10180623973727425
isSimiliarSlope:True
relative_difference:0.33611884865366753
isSimiliarSlope:False
relative_difference:0.059985369422092163
isSimiliarSlope:True
relative_difference:0.6122448979591837
isSimiliarSlope:False
relative_difference:0.4912417282989489
isSimiliarSlope:False
relative_difference:0.04486873508353228
isSimiliarSlope:True
relative_difference:2.0
isSimiliarSlope:False
relative_difference:0.7967097532314925
isSimiliarSlope:False
relative_difference:0.48371174728529115
isSimiliarSlope:False
relative_difference:1.5904
isSimiliarSlope:False
relative_difference:0.30943396226415093
isSimiliarSlope:False
relative_difference:0.5185185185185185
isSimiliarSlope:False
relative_difference:0.547105561861521
isSimiliarSlope:False
relative_difference:1.0447761194029852
isSimiliarSlope:False
relative_difference:0.16205128205128208
isSimiliarSlope:True
relative_difference:1.601246105919003
isSimiliarSlope:False
relative_difference:0.6631853785900784
isSimiliarSlope:False
relative_difference:0.06060606060606061
isSimiliarSlope:True
pngFilePath: C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\sample_result\output\cell_7\output\cell_7_85.0.png
csvFilePath: C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\sample_result\output\cell_7\output\cell_7_85.0.csv
chartFilePath: C:\Users\hongy\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\sample_result\output\cell_7\output\cell_7_85.0_brightness_chart.png
