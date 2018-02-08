###primes from Bnetfiles###

import PyBoolNet
from PyBoolNet import FileExchange

primes = FileExchange.bnet2primes("example01.bnet","example01.primes")	#Erstelle erst in txt-datei den Datensatz im .bnet-Format, nenne es 										example01.bnet. Durch den Befehl bnet2primes werden alle prime 										implicants aus dem .bnet-file erzeugt und in einer neuen Datei 										example01.primes gespeichert

									#>>> primes
									#{'v1': [[{'v1': 1, 'v3': 0}, {'v2': 0}], [{'v2': 1, 'v3': 1}, {'v1': 										0, 'v2': 1}]], 'v2': [[{'v3': 1}], [{'v3': 0}]], 'v3': [[{'v1': 0, 										'v2': 0}], [{'v2': 1}, {'v1': 1}]]}

### Interaction graph ###


primes = FileExchange.read_primes("example01.primes")			#Um den Graphen zu erzeugen lesen wir die Datei example01.primes ein


from PyBoolNet import InteractionGraphs as IGs

									# selbstausgedachtes Netzwerk manuell eingesetzt 
									#bnet = "\n".join(["v1,v1|v3","v2,1","v3,v1&!v2 | !v1&v2"])

primes = FileExchange.bnet2primes("example01.primes")
igraph = IGs.primes2igraph(primes)

igraph.graph["node"]["shape"] = "circle"
igraph.graph["node"]["color"] = "blue"
IGs.add_style_default(igraph)					# fügtinhibitorische und aktivierende Kanten ein
igraph.graph["label"] = "Example 1: First selfconstructed network"
igraph.graph["rankdir"] = "LR"

IGs.igraph2image(igraph,"example02_igraph.pdf")			# speichert erstellten Interactiongraph in einer neuen pdf.

	
							



###State Transition Graph###

from PyBoolNet import StateTransitionGraphs as STGs
from PyBoolNet import FileExchange
#bnet = "\n".join(["v1,v1|v3","v2,1","v3,v1&!v2 | !v1&v2"])
#primes = FileExchange.bnet2primes (bnet)
#asynchronous
update = "asynchronous"
stg = STGs.primes2stg(primes, update,init)
#stg
stg.graph["label"] = "Example 2: The asynchronous network"
stg.graph["rankdir"] = "LR"
STGs.stg2image(stg,"example01_asynchron_stg.pdf")
#synchronous
update = "synchronous"
stg = STGs.primes2stg(primes, update)
#stg
stg.graph["label"] = "Example 2: The asynchronous network"
stg.graph["rankdir"] = "LR"
STGs.stg2image(stg,"example01_synchron_stg.pdf")

