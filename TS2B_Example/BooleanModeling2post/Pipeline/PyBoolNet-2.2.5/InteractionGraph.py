import sys
import argparse
from PyBoolNet import FileExchange
from PyBoolNet import InteractionGraphs as IGs

#inputfile = input('Enter the name of the directory and inputfile:')



parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Enter the directory of the ./TS2B_output/output2.bnet -file")
args = parser.parse_args()
#print(args.dir)



#Enter in command line: python3 InteractionGraph.py ./TS2B_output/TS2B_outputfile.txt 

#For Help: InteractionGraph.py [-h] dir

primes = FileExchange.bnet2primes(args.dir)
igraph = IGs.primes2igraph(primes)
#print(igraph.edges())

sif_string = ""
for (source,dest) in igraph.edges():
	signs = list(igraph.adj[source][dest]["sign"])
	sif_string+= source+" "+str(signs)[1:][:-1]+" "+dest+"\n"
	#print((source,dest))
	#print(igraph.adj[source][dest]["sign"])

#replace "-" back to ".":Because "."in a nodesname causes trouble in PyBoolNet
newsif_string = sif_string.replace("__","_")

outputfile = input('Enter the name of the outputfile: ')
filename ='{}.sif'.format(outputfile)
file = open(filename, "w")
file.write(newsif_string)
#print(newsif_string)
#print(igraph.graph["edge"])





