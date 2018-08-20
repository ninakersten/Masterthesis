# Masterthesis

In this masterthesis the goal is to show a sufficient way to process microarray real-life course-time data and a smaller fictional data set to get a boolean model and analyze the model in an aysnchronous and synchronous manner.

The real-life course-time data is povided by a platform called DREAM-Challengen. The DREAM8 HPN-Breast Cancer Challenge was selected. Due to the fact that in real life experiments serveral cell lines are used and different stimuli and inhibtors it is nessercary to filter the microarray data set into similar experinemtal conditions. 
Here the tool TS2B is used to discretisize (by a k-means clustering algorithm) the data and build a boolean model. This tool comes along with three major algorithms: REVEAL, BESTFIT and FULLFIT.

After the learning step the data is analyzed in a tool called PyBoolNet. PyBoolNet is a nice way to create images of the models and get information about the attractors in a network, the flow in a network and the asynchronous and synchronous properties of a network.

The goal is to connect all these steps in a more fluently way by programming two parser CSV2TXT.R and Boolean2Bnet.R. They should help to transform the original experimental DREAM-CHallenge data into an input file with is compatible with the TS2B tool. And after modelling the output of the TS2B should be transformed from a .txt to a .bnet format.

Furthemore the models of the real-life course-time data are evaluated by a AUROC-Score (Area Under the Curve). Therefore a tool of the DREAM-Challenge platformis provided called DREAMTools, a python package for scoring collaborative challenges. 

First the WORKFLOW for the Example-data is shown and second is the WORKFLOW for the real-life course-time data of the DREAMCHALLENGE.

Requirements:

- Python 3.5.2 (default, Nov 23 2017, 16:37:01)
- Python 2.7.14 ; Anaconda, Inc. (default, Dec  7 2017, 17:05:42)
- R version 3.4.3 (2017-11-30)
- Download the training data set of the DREAM8 - HPN DREAM Breast Cancer Challenge (https://www.synapse.org/#!Synapse:syn5924123).      Here the main not the full experimental data is used. The "main"- dataset has less nodes than the "full"-dataset.
- Install TS2B (https://bioinfocs.rice.edu/ts2b)
- Install PyBoolNet (https://github.com/hklarner/PyBoolNet/releases)

WORKFLOW: for DREAM CHALLENGE data set

### STEP 1: CREATING A BOOLEAN NETWORK ###

#After all installations download the TS2B-folder from this git repository:
#Go to  ./Pipeline$

Rscript CSV2TXT.r

#Output should be stored in "./Pipeline/CSV2TXT_output" 

#Run the TS2B-program:
#Til now, networks can be just created one after another

#Go to ./BooleanModeling2Post$

#Run TS2B (by typing in the commandline): E.g.:
python BinInfer.py input=./Pipeline/CSV2TXT_output/[file_name].txt bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3 > ./Pipeline/TS2B_output/output.txt

#Run the TS2B with at least 3 solutions and a min error of 5. The best combination is BESTFIT in combination with the k-means clustering algorithm.

#The computation the network may take a while. For about 48nodes and the example above about 10minutes.
## ProblemSolvingInProcess ##: Taking the output of TS2B from the terminal is an ugly way to work with such that a solution is in process to transform the TS2B_output into .bnet format directly in the TS2B-algorithm. The progress of this process is stored in a BinInfer.py-file in this git repository.

### STEP 2: CREATING THE INTERACTION GRAPH ###

#Go back to  ./Pipeline$
#Run the Boolean2bnet.r

Rscript Boolean2bnet.r
 
#The product of Boolean2bnet.R is stored in the "/PyBoolNet-2.2.5" -folder

#Run InteractionGraph.py

#./Pipeline/PyBoolNet-2.2.5/
#Run InteractionGraph.py

python3 InteractionGraph.py [directory of the inputfile]

#e.g.: python3 InteractionGraph.py /TS2B/BooleanModeling2post/Pipeline/TS2B_output/output2.bnet > InteractionGraph.sif

#The created .sif file provides information about the edges,like A 1 B (A activates B) and B -1 A (B inactivates A)
#.sif-file is stored in PyBoolNet-2.2.5



- Run The PyBoolNet-Tool:

  e.g.:<br/> 
        $ cd \"directory of the converted file.bnet placed in the PyBoolNet-2.2.5 file\"<br/>
        $ python3<br/> 
      >>> from PyBoolNet import FileExchange<br/> 
      >>> from PyBoolNet import InteractionGraphs as IGs<br/> 
      >>> primes = FileExchange.bnet2primes(\"converted_Boolean2bnet_TS2B_output.bnet\")<br/> 
      >>> igraph = IGs.primes2igraph(primes)<br/> 
      >>> IGs.igraph2image(igraph, \"InteractionGraph.pdf\")<br/> 
      
 - In this git repository the first successful trial with BT20_full_Insulin.pdf can be regarded.   
 - Do this for all cell lines and inhibitor combination: This results in about 32 networks
 - Calculate for all 32 networks the AUROC-score with the help of the DREAM-tools (http://dreamchallenges.org/tools/) and take the mean score of all to compare the result to the other DREAM-Challenge particpants.
 
 ### STEP 3: ASSESSING THE NETWORK ###

#Install DREAMTools (http://dreamchallenges.org/tools/)

git clone git@github.com:dreamtools/dreamtools.git
cd dreamtools                            
pip3 install dreamtools
