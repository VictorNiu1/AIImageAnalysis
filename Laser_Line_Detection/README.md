# Instruction
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
