# generates the .sif input format by creating an Interactiongraph and calculating the edge weights

from PyBoolNet import FileExchange
from PyBoolNet import InteractionGraphs as IGs
primes = FileExchange.bnet2primes("output2.bnet")
igraph = IGs.primes2igraph(primes)
#print(igraph.edges())
sif_string = ""
for (source,dest) in igraph.edges():
	signs = list(igraph.adj[source][dest]["sign"])
	sif_string+= source+" "+str(signs)[1:][:-1]+" "+dest+"\n"
	print((source,dest))
	print(igraph.adj[source][dest]["sign"])

filename = "tset"
file = open(filename, "a")
file.write(sif_string)
file.close()
print(sif_string)
#print(igraph.graph["edge"])
