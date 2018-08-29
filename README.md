# Masterthesis #

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

## WORKFLOW: for DREAM CHALLENGE data set ##

### STEP 1: CREATING A BOOLEAN INTERACTION GRAPH ###

- Download the TSB-file
- Go to ./Pipeline$
- Run the shellscript.sh:

```bash shellscript.sh```#Making the bash script executable: ```chmod 700 shellscript.sh```

### STEP 2: ASSESSING THE NETWORK ###

- Install DREAMTools (http://dreamchallenges.org/tools/)  

```git clone git@github.com:dreamtools/dreamtools.git```    
```cd dreamtools```                                
```pip3 install dreamtools```    

If you are a end-user, you can skip this section and move directly to the scoring section.

For admin, you may need to download some files before using the code e.g., the
aggregation functions. Since you will need to access to synapse to download
those files, you will also need to create a configuration file in your home directory.::

```[authentication]```   
```username: your_email_registered@synapse```    
```password: yourSynapsePassword```    

Then, type::

```from dreamtools.dream8.D8C1 import downloads```  
```d = downloads.GSDownloader()```  
```d.download_experimental()```  

```d = downloads.SubmissionDownloader()```  
```d.download_all()```  

The scoring functions inside **scoring** can be used to obtain the ROC or RMSE
values of a given submissions.

The **ranking** can be used to obtain the rank of a submisson as compared to all other participants.

Format of submissions are explained on https://www.synapse.org/#!Synapse:syn1720047/wiki/
and examples are provided in ./templates directory.

Here is the procedure to get the ROC or RMSE for sub-challenge C8C1A::

```from dreamtools.dream8.D8C1 import scoring```  

```sc1a = scoring.HPNScoringNetwork(sc1a_submissions.zip)```  
```sc1a.compute_all_aucs()```  
```sc1a.get_auc_final_scoring()```  

- Calculate for all 32 networks the AUROC-score with the help of the DREAM-tools (http://dreamchallenges.org/tools/) and take the mean score of all to compare the result to the other DREAM-Challenge particpants.  


## WORKFLOW: for an ExampleData set ##

- Download the "TS2B_Example"- folder 
- Run this Workflow like with the DreamChallenge-data set above with one exception: ./TS2B_Example/... instead of ./TS2B/...

## Quick Practice in PyBoolNet ##

- Run The PyBoolNet-Tool:
 
   e.g.:<br/> 
         $ cd \"directory of the converted file.bnet placed in the PyBoolNet-2.2.5 file\"<br/>
         $ python3<br/> 
       >>> from PyBoolNet import FileExchange<br/> 
       >>> from PyBoolNet import InteractionGraphs as IGs<br/> 
       >>> primes = FileExchange.bnet2primes(\"converted_Boolean2bnet_TS2B_output.bnet\")<br/> 
       >>> igraph = IGs.primes2igraph(primes)<br/> 
       >>> IGs.igraph2image(igraph, \"InteractionGraph.pdf\")<br/> 
       

