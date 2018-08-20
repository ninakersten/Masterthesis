import sys
import argparse
from PyBoolNet import FileExchange
from PyBoolNet import InteractionGraphs as IGs


parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Enter the directory of the ./TS2B_output/output2.bnet -file")
args = parser.parse_args()
print(args.dir)

#Enter in command line: python3 InteractionGraph.py /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/TS2B_output/output2.bnet

#For Help: InteractionGraph.py [-h] dir


primes = FileExchange.bnet2primes(args.dir)
igraph = IGs.primes2igraph(primes)
#print(igraph.edges())

sif_string = ""
for (source,dest) in igraph.edges():
	signs = list(igraph.adj[source][dest]["sign"])
	sif_string+= source+" "+str(signs)[1:][:-1]+" "+dest+"\n"
	print((source,dest))
	print(igraph.adj[source][dest]["sign"])

filename = "test"
file = open(filename, "a")
file.write(sif_string)
file.close()
print(sif_string)
#print(igraph.graph["edge"])





