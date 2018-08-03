# Masterthesis

In this masterthesis the goal is to show a sufficient way to process microarray real-life course-time data and a smaller fictional data set to get a boolean model and analyze the model in an aysnchronous and synchronous manner.

The real-life course-time data is povided by a platform called DREAM-Challengen. The DREAM8 HPN-Breast Cancer Challenge was selected. Due to the fact that in real life experiments serveral cell lines are used and different stimuli and inhibtors it is nessercary to filter the microarray data set into similar experinemtal conditions. 
Here the tool TS2B is used to discretisize (by a k-means clustering algorithm) the data and build a boolean model. This tool comes along with three major algorithms: REVEAL, BESTFIT and FULLFIT.

After the learning step the data is analyzed in a tool called PyBoolNet. PyBoolNet is a nice way to create images of the models and get information about the attractors in a network, the flow in a network and the asynchronous and synchronous properties of a network.

The goal is to connect all these steps in a more fluently way by programming two parser CSV2TXT.R and Boolean2Bnet.R. They should help to transform the original experimental DREAM-CHallenge data into an input file with is compatible with the TS2B tool. And after modelling the output of the TS2B should be transformed from a .txt to a .bnet format.

Furthemore the models of the real-life course-time data are evaluated by a AUROC-Score (Area Under the Curve). Therefore a tool of the DREAM-Challenge platformis provided called DREAMTools, a python package for scoring collaborative challenges. 


WORKFLOW:

- Download the training data set of the DREAM8 - HPN DREAM Breast Cancer Challenge (https://www.synapse.org/#!Synapse:syn5924123).      Here the main not the full experimental data is used. The "main"- dataset has less nodes than the "full"-dataset.
- Install TS2B (https://bioinfocs.rice.edu/ts2b)
- Install PyBoolNet (https://github.com/hklarner/PyBoolNet/releases)

- Run the CSV2TXT-Parser on the one of the 4 cell lines (BT20_main.csv) main experimental data set
- Run the TS2B with at least 3 solutions and a min error of 5. The best combination is BESTFIT in combination with the k-means clustering algorithm.
- Take the output of the TS2B and run the Boolean2bnet- Parser to convert the the TS2B-output to a PyBoolNet-input-format

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
