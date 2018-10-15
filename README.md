# Masterthesis #

This git repository contains two pipelines "Pipeline_insilico" and "Pipeline_realdata". Both are created to show the application of three well known boolean inference algorithms: REVEAL, BESTFIT and FULLFIT in combination with a k-means clustering algorithm (d= depth of clustering ; can be 1,2,3...or 10). Finally the inferred networks are scored against a goldstandard data set, either created itself (insilico_goldstandard) or provided by prior knowledge from other networks and literature based information (realdata_goldstandard).

The real-life time-course data is povided by a platform called DREAM-Challenge. The DREAM8 HPN-Breast Cancer Challenge was selected. Due to the fact that in real life experiments serveral cell lines are used and different stimuli and inhibtors, it is nessercary to filter the microarray data set into similar experinemtal conditions. Thus four cell lines in combination with 8 stimuli yield a data set of 32 contexts to be inferred and assessed. Here the SubChallenge 1A is considered, by inferring the edges of a network with its dependecies (without the edge confidence= edge weight).




Requirements:

- Python 3.5.2 (default, Nov 23 2017, 16:37:01)
- Python 2.7.14 ; Anaconda, Inc. (default, Dec  7 2017, 17:05:42)
- R version 3.4.3 (2017-11-30)
- Download the training data set of the DREAM8 - HPN DREAM Breast Cancer Challenge (https://www.synapse.org/#!Synapse:syn5924123). Here the main not the full experimental data is used. The "main"- dataset has less nodes than the "full"-dataset.
- Install PyBoolNet (https://github.com/hklarner/PyBoolNet/releases)

## WORKFLOW: for DREAM CHALLENGE data set ##

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
       

