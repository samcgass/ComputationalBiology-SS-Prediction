------------------
Usage Instructions
------------------
This program was create on Windows.
From the command line, PredictSS.py takes two command line arguements.
The first is the model as a pickle file, the second is the .pssm file to be predicted.
The model is provided, it is the SSmodel.pkl file.

To run the program, from the command line type:		python PredictSS.py SSmodel.pkl [filename].pssm
Note: the .pssm file should be in the same directory as PredictSS.py.

The program will create a file in the same directory with the name [filename]_prediction.ss
This file is in the same format as the .ss files and it contains the given model's predicted outputs.

TrainingSS.py is the program that creates the SSmodel.pkl file.
There is no need to run it as I have already run it on my machine and its output, SSmodel.pkl, is given.

When TrainingSS.py is run, it outputs the Q3 accuracy for the model it produces.
The Q3 accuracy it output for the model it produced, SSmodel.py, is copy and pasted below.

Model Complete
______________________________
Correct:  3528
Incorrect:  1989
Total:  5517
______________________________
Model Accuracy:  0.6394779771615008