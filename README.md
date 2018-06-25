# Masterthesis

In this masterthesis the goal is to show a sufficient way to process microarray real-life course-time data and a smaller fictional data set to get a boolean model and analyze the model in an aysnchronous and synchronous manner.

The real-life course-time data is povided by a platform called DREAM-Challengen. The DREAM8 HPN-Breast Cancer Challenge was selected. Due to the fact that in real life experiments serveral cell lines are used and dirfferent stimuli and inhibtors it is nessercary to filter the microarray data set into similar experinemtal conditions. 
Here the tool TS2B is used to discretisize (by a k-means clustering algorithm) the data and build a boolean model. This tool comes along with three major algorithms: REVEAL, BESTFIT and FULLFIT.

After the learning step the data is analyzed in a tool called PyBoolNet. PyBoolNet is a nice way to create images of the models and get information about the attractors in a network, the flow in a network and the asynchronous and synchronous properties of a network.

The goal is to connect all these steps in a more fluently way by programming two parser CSV2TXT.R and Boolean2Bnet.R. They should help to transform the original experimental DREAM-CHallenge data into an input file with is compatible with the TS2B tool. And after modelling the output of the TS2B should be transformed froma .txt to a .bnet format.

Furthemore the models of the real-life course-time data are evaluated by a AUROC-Score (Area Under the Curve). Therefore a tool of the DREAM-Challenge platformis provided called DREAMTools, a python package for scoring collaborative challenges. 

