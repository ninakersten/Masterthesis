#primes from Bnetfiles
import PyBoolNet
from PyBoolNet import FileExchange
primes = FileExchange.bnet2primes("example01.bnet")
#primes
#{'v1': [[{'v1': 1, 'v3': 0}, {'v2': 0}], [{'v2': 1, 'v3': 1}, {'v1': 0, 'v2': 1}]], 'v2': [[{'v3': 1}], [{'v3': 0}]], 'v3': [[{'v1': 0, 'v2': 0}], [{'v2': 1}, {'v1': 1}]]}
primes = FileExchange.bnet2primes("example01.bnet","example01.primes")
#created example01.primes
primes = FileExchange.read_primes("example01.primes")
FileExchange.write_primes(primes,"example01.primes")
#created example01.primes
FileExchange.primes2bnet(primes, "example01.bnet")
#created example01.bnet



### Interaction graph ###

from PyBoolNet import InteractionGraphs as IGs
# selbstausgedachtes Netzwerk eingesetzt
bnet = "\n".join(["v1,v1|v3","v2,1","v3,v1&!v2 | !v1&v2"])
primes = FileExchange.bnet2primes(bnet)
igraph = IGs.primes2igraph(primes)
igraph
#<networkx.classes.digraph.DiGraph object at 0x7f3c302f8d50>
IGs.igraph2image(igraph, "example02_igraph.pdf")
created example02_igraph.pdf
bnet = "\n".join(["v1,v1&!v3&v2","v2,!v1","v3,v3&v2"])
primes = FileExchange.bnet2primes(bnet)
igraph = IGs.primes2igraph(primes)
igraph
#<networkx.classes.digraph.DiGraph object at 0x7f3c1c1a3950>
IGs.igraph2image(igraph, "example01_igraph.pdf")
#created example01_igraph.pdf
# Interaction graph stimmt mit gezeichneten Graphen überein^^

###State Transition Graph###

from PyBoolNet import StateTransitionGraphs as STGs
from PyBoolNet import FileExchange
bnet = "\n".join(["v1,v1|v3","v2,1","v3,v1&!v2 | !v1&v2"])
primes = FileExchange.bnet2primes (bnet)
#asynchronous
update = "asynchronous"
stg = STGs.primes2stg(primes, update)
stg
STGs.stg2image(stg,"example01_stg.pdf")
#synchronous
update = "asynchronous"
stg = STGs.primes2stg(primes, update)
stg
STGs.stg2image(stg,"example01_stg.pdf")

