#!/bin/bash
### Bash-Script for DREAMChallenge C8D1 ### (Nina Kersten)

#Register on Synapse (https://www.synapse.org/)
#Register on Git (https://github.com/)
#Download the trainig data set of the DreamChallenge C8D1 (https://www.synapse.org/#!Synapse:syn5924123)
#	directory to the data in the training data set folder:  "/Training data/experimental/experimental/CSV/["CellLineName"]_full.csv"
#	4 "celllines" with 8 stimuli in each cellline, means: 8 experiments with each cellline yields 32 networks
#Install TS2B (https://bioinfocs.rice.edu/ts2b)
#Install PyBoolNet (https://github.com/hklarner/PyBoolNet/releases)
#Install Python Synapse Client (https://github.com/Sage-Bionetworks/synapsePythonClient)

#sudo pip3 install synapseclient[pandas,pysftp]

#Requirements:	Python 3.5.2 (default, Nov 23 2017, 16:37:01)
#		Python 2.7.14 |Anaconda, Inc.| (default, Dec  7 2017, 17:05:42) 
#		R version 3.4.3 (2017-11-30)
################################################################################################################################################


### STEP 1: CREATING A BOOLEAN NETWORK ###

#Go to  ./BooleanModeling2post$


Rscript ./Pipeline/CSV2TXT.r


#Run the TS2B-program:

#E.g.:
	
python BinInfer.py input= ./Pipeline/CSV2TXT_output/BT20_mainEGF.txt bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3 > ./Pipeline/TS2B_output/output.txt

#Run the TS2B with at least 3 solutions and a min error of 5. The best combination is BESTFIT in combination with the k-means clustering algorithm.



### STEP 2: CREATING THE INTERACTION GRAPH ###

#Run boolean2bnet.R by adapting the goal-directory thus the product of Boolean2bnet.R is stored in the "/PyBoolNet-2.2.5" -folder
#Run InteractionGraph.py

#python3 InteractionGraph.py

#The crated .sif file provides information about the edges,like A 1 B (A activates B) and B -1 A (B inactivates A)




### STEP 3: ASSESSING THE NETWORK ###

#Install DREAMTools (http://dreamchallenges.org/tools/)

#git clone git@github.com:dreamtools/dreamtools.git
#cd dreamtools                            
#pip3 install dreamtools
   


