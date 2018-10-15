import sys
import argparse
from PyBoolNet import FileExchange
from PyBoolNet import InteractionGraphs as IGs
import os.path


parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Enter the directory of the ./TS2B_output/output2.bnet -file")
args = parser.parse_args()


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
#print(newsif_string)

newname = ' '.join(sys.argv[1:])
outputfile = newname.replace('./bnet_data_insilico/','').replace('.bnet','')
#outputfile = input('Enter the name of the outputfile: ')

filename ='{}.sif'.format(outputfile)

save_path = './goldstandard_insilico/'
completeName = os.path.join(save_path, filename)  
write_bnet_file = open(completeName,"w")
write_bnet_file.write(newsif_string)
write_bnet_file.close()
 
