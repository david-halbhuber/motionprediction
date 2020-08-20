# Predicting Avatar Movement in Virtual Reality using Neural Networks
![Starting Scene](https://github.com/Cele3x/practical-seminar/blob/master/submission/Images%20General/teaser.PNG)
This repository was used for the project "Predicting Avatar Movement in Virtual Reality using Neural Networks" carried out as part of the course "Praxisseminar" in the summer semester 2019 at the University of Regensburg. 
Furthermore, this repository will be used to submit the final product. 

For the actual submission only the folder __submission__ , found in the root directory of this repository, is relevant. The folder contains several subfolders, sorted alphabetically: 
- [Data Acquisiton Study](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Data%20Acquisiton%20Study)
- [Docs](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Docs)
- [Evaluation Study](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Evaluation%20Study)
- [Images General](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Images%General)
- [Intercepter Client](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Intercepter%20Client)
- [Latency Test Framework](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Latency%Test%Framework)
- [Neural Network](https://github.com/Slimboy-90/motionprediction-/tree/master/submission/Neural%Network)


Each subfolder will be described in the following, starting with __Data Acquisition Study__: 

## Data Acquisiton Study
This folder contains all the material needed and obtained for and during the data acquisiton study. It does NOT contain the acutal gathered data for the coresponding participant, since this is not possible due to GitHubs size limitation for repositories. The actual data will be submitted seperatly on an USB devices. It is structured as follows: 
- Demographics: Contains a list of the demographics of all study participants, as well as some information about whether they were wearing glasses or not. Additionally it contains information about previous experience in VR and sportiness of the participants. 
- Video: Showing one voluniteer participanting in the conducted acquisiton study. Consense to show the video was obtained. 


## Docs 
This folder comprises two subfolder with the following containment:
- Paper: Final version of the scientific paper written during the project. 
- Projekt Handbuch: This is a document which elabroates how to use the developed movement prediciton system. It, as well, explaines a bit more technical back ground compared to the presented paper above. Additonally it grants deeper insight in the developed and presented Latency Test Framework. 

## Evaluation Study 
This folder contains all data gathered during the evaluation study. It also contains the measured results for the questionnaire and the performance task. It does not contain or discuss any results or findings, please see the submitted paper for findings, results and a conclusion. 
- Demographics: Contains a list of the demographics of all study participants, as well as some information about whether they were wearing glasses or not. Additionally it contains information about previous experience in VR and sportiness of the participants.
- Perfomance Data: Contains the measurements of the conducted Perfomance task. 
- Questionnaire Data: Contains the gathered results of the asked questionnaire. 
- Unity Project: Contains the used Unity 3D Scene used to evaluated the presented system and to collect questionnaire data as well as perfomance data. Instructions on how to use the application can be found here: [README](https://github.com/Slimboy-90/motionprediction-/tree/master/04-user-study/src/README.md)

## Image General
This folder contains all needed image for this repository, as well as all images needed for the paper and the "Projekt Handbuch". 

## Intercepter Client
This folder is used for the developed Intercepter Client and all its dependencies, its containment is structured as follows: 
- GuiClient: Graphical user interface for intercepting stream data and changing prediction models.
- CSVClient: Command line tool for reading and writing motive stream data to a CSV file. (First Draft)


## Latency Test Framework
This folder contains everything needed to conduct the in the paper described latency tests. The content is organized as shown below:
- Arduino Sketches: The sketches used to run the LTF can be found here. There are two seperated folders, one containing the early test variant to establish a connection between an external computer and the Arduino. The second script is the actual script used to measure latency. It connects one digital sensor and one analog sensor, waits for the to trigger and sends the corresponding event to the connected external computer. 
- Python Scripts: This folder contains the script to obtain information from the arduino. This script gathers the two distinc timestamps received from the Arduino, compares them and prints a latency value to the console and a CSV file. 

## Neural Network 
This folder contains everything related to the used neural network, it is structured as shown in the following: 
- Data-Handling: Contains all scripts needed to handle the data gathered in the data acquisiton study. 
- Evaluation: Contains all scripts needed for evaluating the presented neural network. 
- Models: Contains all trained models, even those not evaluated in the evaluation study. 
- Training: Contains all scripts needed for training the presented neural networks. 

Does NOT contain the virtual enviroment used. Please make sure you have python 3.7.X and the needed packages installed. 
