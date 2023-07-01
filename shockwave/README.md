# Instruction
Python script to segment multiple cell and calculate the signal on each cell
## Get help
PS C:\Users\changfan\Documents\GitHub\AIImageAnalysis\shockwave> python data_analysis.py --help

       USAGE: data_analysis.py [flags]
flags:                                                                    
                                                                          
data_analysis.py:                                                         
  --folder: Stuart SFR raw image filename                                 
    (default:                                                             
    'C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922
    FOV5\\Fluo4')                                                         
## Example on how to run the data analysis                                                                        
python data_analysis.py --folder "C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922\\FOV5\\Fluo4"

## result
I0516 22:50:54.656602 47196 data_analysis.py:105] save the shock wave image to -> C:\Users\changfan\Documents\GitHub\AIImageAnalysis\data\101922_FOV5\Fluo4\output\brightness.png
I0516 22:50:54.656602 47196 data_analysis.py:106] ================================================= Finish image analysis =================================================
(venv) PS C:\Users\changfan\Documents\GitHub\AIImageAnalysis\shockwave> python data_analysis.py --folder "C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922_FOV5\\Fluo4"
I0516 22:51:21.005316 53196 data_analysis.py:30] ================================================== Start image analysis ==================================================
I0516 22:51:21.006315 53196 data_analysis.py:31] -------------------------------------------------- detect the brightest frame --------------------------------------------
I0516 22:51:23.802726 53196 data_analysis.py:41] The index of maximum frame is -> 50
I0516 22:51:23.802726 53196 data_analysis.py:43] -------------------------------------------------- detect cell on the brightest frame ------------------------------------
I0516 22:51:23.820725 53196 data_analysis.py:53] save the roi coordinator to   -> C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922_FOV5\\Fluo4\output\ROIs.csv
I0516 22:51:23.895725 53196 data_analysis.py:68] save the roi image to         -> C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922_FOV5\\Fluo4\output\roi.png
I0516 22:51:23.896727 53196 data_analysis.py:70] -------------------------------------------------- calculate the roi signal on each frame --------------------------------
I0516 22:51:26.350604 53196 data_analysis.py:85] save the roi signal to        -> C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922_FOV5\\Fluo4\output\brightness.csv
I0516 22:51:31.852896 53196 data_analysis.py:105] save the shock wave image to -> C:\\Users\\changfan\\Documents\\GitHub\\AIImageAnalysis\\data\\101922_FOV5\\Fluo4\output\brightness.png
I0516 22:51:31.853895 53196 data_analysis.py:106] ================================================= Finish image analysis =================================================
