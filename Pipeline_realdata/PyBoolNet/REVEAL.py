"""REVEAL.py: Description of what foobar does."""
__author__      = "Natalie Berestovsky, Rice University"

from bitarray import bitarray
import itertools, random
from math import log
from utilsS2B import KarnaughMaps


debug = False
	
def intpuEntropiesDeterministic(keys, tt):
	# create combinations for the list of entropies
	combinations = []
	for i in range(1, len(keys)+1):
		a = itertools.combinations(keys, i)
		for ak in a:
			combinations.append("".join(ak))
	allE = {}
	# for each combination find entropy
	for c in combinations:
		p = itertools.product("01", repeat=len(c))
		totals = []
		for p1 in p:
			finalOuts = list(tt.keys())
			'''# ---- THIS INCLUDES Inputs with multiple Outputs, len(outputs) times----
			for kkk,l in tt.items():
				if len(l) > 1:
					for ll in range(len(l)-1):
						finalOuts.append(kkk)
			'''

			for k in tt.keys():
				# that is done by matching the idx
				for idx in range(len(c)):
					character = c[idx]
					value = p1[idx]
					position = keys.index(character)
					if int(k[position]) != int(value):
						'''# ---- This removes multiple outputs if needed (all of them) - needed if adding things arount the line 115
						zz = finalOuts.count(k)
						#for zzz in range(zz):'''
						finalOuts.remove(k)
						break
			#print len(consideredOuts), len(finalOuts)
			totals.append(len(finalOuts))
		if debug:
			print totals
		s = float(sum(totals))
		#counted all permutations, now calc entropy
		entr = 0
		for t in totals:
			if t != 0:
				entr -= t/s * log(t/s,2)
		allE["".join(c)] = entr
		
	return allE


def outputEntropy(item, keys, tt, inputE, allE, level):
	# calculate single output entropies H(A')
	# items position in the key
	iidx = keys.index(item)
	combinations = itertools.combinations(keys, level)
	for c in combinations:
		totals = []
		for bin in range(2):
			# since item is output, we are seeing if it has the right value in the OUTPUTS, not keys
			consideredIns = []
			for k in tt.keys():
				for kk in tt[k]:
					if int(kk[iidx]) == bin:
						consideredIns.append(k)
			#print item,c,bin
			p = itertools.product("01", repeat=level)
			for p1 in p:
				finalList = list(consideredIns)
				#print p1, finalOuts
				
				for k in consideredIns:
					# that is done by matching the idx
					for idx in range(len(c)):
						character = c[idx]
						value = p1[idx]
						position = keys.index(character)
						#print character, value, position, int(k[position]), k
						if int(k[position]) != int(value):
							finalList.remove(k)
							break
				#print len(consideredOuts), len(finalOuts)
				totals.append(len(finalList))
		if debug:
			print totals		
		s = float(sum(totals))
		#counted all permutations, now calc entropy
		entr = 0
		for t in totals:
			if t != 0:
				entr -= t/s * log(t/s,2)
		allE[item+"\'"+"".join(c)] = entr
	return allE

def calculateM(item, keys, inputE, allE, level):
	if (level == 0):
		return
	allMs = {}
	iidx = keys.index(item)
	combinations = itertools.combinations(keys, level)
	for c in combinations:
		comb = "".join(c)
		entr1 = allE[item+"\'"]
		entr2 = inputE[comb]
		
		entrBoth = allE[item+"\'"+comb]
		#print item, c, item, entr1, comb, entr2, entrBoth
		m = entr1 + entr2 - entrBoth
		if entr1 == 0:
			m = 0
		else:
			m /= entr1
		allMs[item+"\'"+comb] = m

	return allMs

'''
data: key is the name of interactions, item is the function dictionary
used to extract a complete rule table for individual species
'''
def getText(data):
	toInterprete = {}
	texts2return = []
	
	for name in data.keys():
		func = data[name]
		
		o,i = name.split("\'")
		if len(i) > 3:		# only interpprete function with 3 or less inputs
			print str(name)+": Input is too large "
			continue

		# check completeness and get the final list of what to interprete
		p = itertools.product("01", repeat=len(i))
		good = True	#assume it's a good table
		for p1 in p:
			valp1 = "".join(p1)
			zeroOut = func[0]
			oneOut = func[1]
			if valp1 not in zeroOut and valp1 not in oneOut:
				#print "Incomplete transition "+str(name)+" "+str(func)
				good = False
				break
		if good:
			toInterprete[name] = func

	km = KarnaughMaps()
	allTexts = {}
	for name, func in toInterprete.items():
		#print name, func
		o,i = name.split("\'")

		if len(i) == 1:
			f = km.getFunction1(name, func)
		elif len(i) == 2:
			f = km.getFunction2(name, func)
		elif len(i) == 3:
			f = km.getFunction3(name, func)
		
		if o in allTexts:
			allTexts[o].append(f)
		else:
			allTexts[o] = [f]
			
	for zz in range(100):
		text = ''
		for k in allTexts.keys():
			rText = random.choice(allTexts[k])
			if rText != '':
				text += random.choice(allTexts[k]) +'\n'
		if text not in texts2return and text != '':
			texts2return.append(text)
	return texts2return