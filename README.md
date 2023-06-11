# UCSDAIProject
AI Project for UCSD

## Project Description
This project uses a Reinforcement Learning Neural Network called DDPG to 
perform automatic analysis of a dataset provided by UCSD. The dataset is comprised of [data description]
and also contains a CNN intended to perform semantic segmentation of the TIFF images
provided by UCSD. The CNN is trained on the dataset and then used to generate an image of the
same resolution that has everything besides the target area blacked out. 
The DDPG neural network is then trained in an environment containing the pre-cut and
post-cut images with the goal being to compute the distance of the axons after the cut.

## Concept Description
### Reinforcement Learning
Reinforcement Learning is a branch of machine learning that teaches a machine what to do
based on an actor-critic system. The actor is the neural network that takes in the state of the
environment and outputs an action. The critic is the neural network that takes in the state of the
environment and outputs a value. The critic is used to train the actor by telling it how good of a
decision it made. The actor is then used to make decisions in the environment. To put this in an analogy:
imagine you are watching an actor play a role in a film. The actor (our neural network) will act, play the role, etc...
The critic will then tell the actor what it could've done better, thereby informing the actor on how to do it better the next time.
The actor does some action (in this case it would be measuring the distance of the cut) and the critic
tells the actor what could've been better (like measure the cut closer to this axon to be more accurate or something like that)

### Convolutional Neural Network/Semantic Segmentation
A Convolutional Neural Network (CNN) is a type of neural network that is used for analyzing images. I won't explain
the process of how a CNN works here, but I will explain how it is used in this project. The CNN is given pairs of images:
one image containing the full area and the other image containing the manually segmented out image that only includes the target area.
The CNN will use these image pairs to take an unsegmented image in the future and then segment it down to
the target area.

### Environment for Reinforcement Learning
The environment we are using for the Reinforcement Learning is a custom environment that is built using Keras. When I say
"environment" it might sound confusing so to simplify it lets bring back the actor in a film analogy.
The environment is the set that the actor is in. That is all. In this case, the environment is the image of the axons before and after the cut.
The actor is the neural network that is trained to measure the distance of the cut. The critic is the neural network that is trained to tell the actor how
to measure the distance more accurately. This all simply happens within the training environment.


### How the Neural Networks Relate
The CNN is used to generate the images that contain only the target areas that will be used to train the Reinforcement 
Learning Neural Network (DDPG). Therefore, the output of the CNN is the input to the DDPG. The CNN will be used to
segment any future images as well and those segmented images will then have the distance when the axons are cut computed by
the DDPG (reinforcement learning) neural network. 

### How the DDPG Neural Network Works
I won't go into the mathematics of it or the in-depth computer science behind it, but I will just give a general explanantion of how
it works so the code might be better understood. There are two neural networks inside the DDPG neural network. 
One neural network is the actor's neural network: a network designed to perform an action based on an input.
The other neural network is the critic's neural network, which is designed to critique the actor's performance by assigning
it a value based on how well it did (think of this as similar to giving the actor a rating from 1-10). 
The actor then performs differently based on the advice from the critic. 

## How to Run the Code
### Installing Python/Anaconda/Packages (Windows)
1. Install Anaconda (https://repo.anaconda.com/archive/Anaconda3-2022.10-MacOSX-arm64.pkg)
2. Open Anaconda Navigator (what you just installed)
3. Click on "Environments" on the left side of the screen
4. Click on "Create" at the Bottom left side of the screen
5. For name say "UCSDAIProject"
6. For Packages click check on "Python" and make the version 3.8.16
7. Click "Create"
8. Now click on the green arrow that is to the right of the name of the environment
9. Now click "Open Terminal"
10. In the terminal window then type out these commands (type "y" for every prompt that comes up):
```
conda install -c conda-forge -c powerai gym=0.26.1
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
python -m pip install "tensorflow<2.8.0"
conda install numpy=1.23.5
conda install  matplotlib=3.6.2
conda install keras=2.8.0
``` 
11. Now install Visual Studio Code (https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal)
12. Open Visual Studio Code
13. In Visual Studio Code hit Extensions (its the final icon on the left panel)
14. Now install Python
15. Install Github Desktop (https://central.github.com/deployments/desktop/desktop/latest/darwin)
16. Open Github Desktop
17. In Github Desktop click on "Clone a repository from the internet" (Keep in mind you will need to have a Github account)
18. Then hit "URL" and put in this link: https://github.com/VictorNiu1/AIImageAnalysis
19. Now just hit "Clone"
20. Hit Open in Visual Studio Code
21. Once Visual Studio Code Opens hit "Trust the authors of all files in the parent folder 'GitHub'" and then click "Yes, I trust the authors"
22. Then hit Select Python Interpretor and then click on UCSDAIProject
23. Okay now click on the models folder and then click on the DDPG.py file
24. Now click on the arrow in the upper right corner and watch it run in the terminal!

### Installing Python/Anaconda/Packages (M1 Mac)
1. Install Anaconda (https://repo.anaconda.com/archive/Anaconda3-2022.10-MacOSX-arm64.pkg)
2. Open Anaconda Navigator (what you just installed)
3. Click on "Environments" on the left side of the screen
4. Click on "Create" at the Bottom left side of the screen
5. For name say "UCSDAIProject"
6. For Packages click check on "Python" and make the version 3.8.16
7. Click "Create"
8. Now click on the green arrow that is to the right of the name of the environment
9. Now click "Open Terminal"
10. In the terminal window then type out these commands (type "y" for every prompt that comes up):
```
conda install -c apple tensorflow-deps
python3 -m pip install tensorflow-macos==2.9.0
python3 -m pip install tensorflow-metal==0.5.0
python3 -m pip install gym==0.25.2
python3 -m pip install matplotlib==3.6.2
python3 -m pip install numpy==1.24.2
python3 -m pip install opencv-python==4.7.0.72
``` 
11. Now install Visual Studio Code (https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal)
12. Open Visual Studio Code
13. In Visual Studio Code hit Extensions (its the final icon on the left panel)
14. Now install Python
15. Install Github Desktop (https://central.github.com/deployments/desktop/desktop/latest/darwin)
16. Open Github Desktop
17. In Github Desktop click on "Clone a repository from the internet" (Keep in mind you will need to have a Github account)
18. Then hit "URL" and put in this link: https://github.com/VictorNiu1/AIImageAnalysis
19. Now just hit "Clone"
20. Hit Open in Visual Studio Code
21. Once Visual Studio Code Opens hit "Trust the authors of all files in the parent folder 'GitHub'" and then click "Yes, I trust the authors"
22. Then hit Select Python Interpretor and then click on UCSDAIProject
23. Okay now click on the models folder and then click on the DDPG.py file
24. Now click on the arrow in the upper right corner and watch it run in the terminal!


## How to Run czi to tiff
1. Download czi file and put it in your GitHub folder under AIImageAnalysis
2. Open the csv file named "bpconfig_czi2tiff.csv" (changing the things in this csv file will change the output)
3. Rename the first item to the name of the czi file
4. Change second value to 1 so that it actually outputs the tiff files (1 means it actually outputs files, 0 means no output)
5. 3rd value is for the formatting of the name of the file, if set to 0, 1, 2, or 3 the frame number will be at the start of the file name and 4, 5, 6, or 7 will put the frame number at the end. 0 and 4 would mean only the frame number is included, 1 and 5 would be frame number and duration, 2 and 6 would be only the frame number and date, and 3 and 7 would be the frame number as well as both the date and duration.
6. go to czi2tiff.py and hit run!
