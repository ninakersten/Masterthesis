#!/usr/bin/env python
"""
An example of how to interact with the plotting canvas by connecting
to move and click events
"""
import sys, os, itertools, random, math, numpy, pickle
from operator import itemgetter, attrgetter
from bitarray import bitarray
from utilsS2B import Binarization, KarnaughMaps, BestFit
import REVEAL
from boolean2 import Model, util
from subprocess import Popen, PIPE, STDOUT
from time import time

allOSeries = []
allBSeries = []
originalSeries = {}	# original series stored here as a list
binarySeries = {}	# structure same as the original but with binary series
inputoutput = {}	# keys are combinations, with a list of compbinations that are outputs of it
debug = False
binz = Binarization()



argumentsValues = {'input':'','iterations':5000, 'maxscore':0,'solutions':1,'output':['score','text'],'verbose':1, 'learn-method':'REVEAL',  'bin-method':3, 'reduction':0}

def main(argv=sys.argv):	
	global argumentValues
	bestBinarySeries = None
	bestScore = None
	bestSums = None
	bestText = None
	bestCompleteSTT = None
	allScores = None
	
	output = {'binSer':bestBinarySeries,'score':bestScore,'sums':bestSums,'text':bestText,"stt":bestCompleteSTT,'allScores':allScores}
		
	dirArg = []
	for arg in sys.argv:
		if ".py" not in arg and "=" not in arg:
			raise TypeError("incorrect argument "+arg)
			break
		if ".py" not in arg:
			name,val = arg.split("=")
			if name == 'input' or name == 'learn-method':
				argumentsValues[name] = val
			elif name == 'iterations' or name == 'solutions' or name == 'verbose' or name == 'reduction':
				argumentsValues[name] = int(val)
			elif name == 'bin-method':
				if val.isdigit():
					argumentsValues[name] = int(val)
				elif val == 'A':
					argumentsValues[name] = 0
				else:
					argumentsValues[name] = 3 # k-means with 3 levels
			elif name == 'maxscore':
				argumentsValues[name] = float(val)
			elif name == 'output':
				# configure output
				argumentsValues[name] = val.split(',')
				
				
	
	namez = argumentsValues['input'].split(',')
	for n in namez:
		if argumentsValues['input'].endswith("pkl"):
			s = pickle.load(open(n, "rb"))
			for k,j in s.items():
				originalSeries[k] = j
			order = originalSeries.keys()
		else:
			f = open(n, 'r')
			topLine = f.readline().split()
			order = []
			for t in topLine:
				originalSeries[t] = []
				order.append(t)
			for line in f:
				if line.startswith("#"):
					continue
				words = line.split()
				for i in range(len(words)):
					originalSeries[order[i]].append(float(words[i]))
		allOSeries.append(originalSeries)
	
	print argumentsValues
	allConvergence = []
	
	allTimes = []
	bMethod = argumentsValues['bin-method']
	for o in allOSeries:
		bSer = None
		if bMethod == 0:
			bSer = binz.BASC_A_binarization(dict(originalSeries), argumentsValues['reduction'])	
		allBSeries.append(bSer)
		
	for i in range(argumentsValues['solutions']):
		print 'Cycle ', i
		
		if argumentsValues['learn-method'] == 'REVEAL':
			conv = findOne_REVEALSolution(argumentsValues['iterations'],argumentsValues['maxscore'],output,binarySeries=allBSeries)
		else:
			conv = findOne_BESTFULLFITSolution(argumentsValues['iterations'],argumentsValues['maxscore'],output,binarySeries=allBSeries,lMethod=argumentsValues['learn-method'])

		
		# record individual solution
		allConvergence.append(conv)
		output['allScores'] = conv
		#findKMeansSolution(output)
		print "\nSolution found:"
		toPrint = argumentsValues['output']
		for tp in toPrint:
			if tp in output:
				print output[tp]
		# reset solution
		output['score'] = None
		output['sums'] = None
		output['text'] = None
		output['binSer'] = None
		output['stt'] = None
		output['allScores'] = None
	#print allConvergence
	#idxOfDot = argumentsValues['input'].index('.')
	#output = open(argumentsValues['input'][0:idxOfDot]+"_"+argumentsValues['learn-method']+str(argumentsValues['bin-method'])+'_multi100.pkl', 'wb')
	#pickle.dump(allConvergence, output)
	#output.close()	
	'''
	else:
		if bMethod == 0:
			print 'BASC A'
			if argumentsValues['learn-method'] == 'BESTFIT':
				solutions = findAllBASCA_BESTFITSolutions()
			elif argumentsValues['learn-method'] == 'ENUM':
				print "soon"
			else:
				solutions = findAllBASCA_REVEALSolutions()
			
			# print all the soltuons
			for sol in solutions:
				text,score = sol
				print score
				print text
			
		elif bMethod == 1:
			print 'BASC B'
		else:
			print 'Unidentified binariztion method. See README.'
	'''
	
			
def findOne_REVEALSolution(maxIters, goodScore, output,binarySeries=None):
	convergence = []
	#for xyz in range(maxIters):
	xyz = 0
	bMethod = argumentsValues['bin-method']
	if bMethod > 0:
		clusters = int(math.pow(2,bMethod))
	
	
	while (output['score'] > goodScore or output['score'] == None):
		if xyz >= maxIters:
			break
		xyz +=1
		if output['score'] != None and output['score'] <= goodScore:
			if argumentsValues['verbose'] >= 1:
				print "STOP since reached score of "+str(goodScore)+" in "+str(xyz) + " iterations"
			break
		if argumentsValues['verbose'] >= 1 and xyz % 100 == 0: 
			print "ITERATIONS "+str(xyz)
			print output['score']
			print output['text']
		# only if we are doing k-means, we have re-binarize every time
		BSeries = []
		for o in allOSeries:
			if bMethod > 0:
				BSeries.append(binz.decrementalKMeanBinarization(dict(o), clusters, argumentsValues['reduction']))	
		
		# otherwise, just battle non-determanism
		allKeys, allFrq, allTransitions = binz.stateTTMostFreq(BSeries)
	
		'''get the initial state for this division'''
		allIStates = []
		for b in BSeries:
			initialState = {}
			for k in allKeys:
				initialState[k] = bool(b[k][0])
			allIStates.append(initialState)
		'''execute binary using the transition table'''
	
		for transitions in allTransitions:
			#print transitions
			entropy = REVEAL.intpuEntropiesDeterministic(allKeys, transitions)
		
			resovled = {}
			unresolved = BSeries[0].keys()
			allEntropy = {}
	
			myIteration = {}
			#limit search to 3 inputs max
			for i in range(0,4):
		
				newUnresolved = list(unresolved)
				for un in newUnresolved:
					if debug:
						print "Resolving "+un+" at level "+str(i)
					allEntropy = REVEAL.outputEntropy(un, allKeys, transitions, entropy, allEntropy, i)
					m = REVEAL.calculateM(un, allKeys, entropy, allEntropy, i)
					if m != None:
						for a,b in m.items():
							if debug:
								print "..."+str(a)+": "+str(b)				
							if abs(b-1) < 0.000000001:
								if un in unresolved:
									unresolved.remove(un)
								x,y = a.split("\'")
								myT = binz.getTTFunction(y,x,transitions, allKeys)
								if debug:
									print myT
								myIteration[a] = myT
		
			allTexts = REVEAL.getText(myIteration)
			bestText = ''
			bestScore = 10000
			
			for text in allTexts:
				sums = {}
				for k in allKeys:
					sums[k] = 0
				for b in BSeries:
					header = ''
					for i in allKeys:
						header += i + " = " + str(allIStates[BSeries.index(b)][i]) + "\n"
					textSim = header + text
					model = Model( mode='sync', text=textSim )
				
					length = len(b[allKeys[0]])
					model.initialize()
					model.iterate( steps=length-1 )
					count = 0
					#compare the binary series
				
					for d in model.states:
						for k in d.keys():
							sums[k] += abs(b[k][count] - int(d[k]))
						count += 1
				score = 0
				for s,v in sums.items():
					score += v
				score /= (float(len(binarySeries[binarySeries.keys()[0]])) * float(len(sums)))
				if score < bestScore:
					bestScore = score
					bestText = textSim
	
			convergence.append(bestScore)			
			if output['score'] is None or bestScore < output['score']:
				output['score'] = bestScore
				#output['sums'] = sums
				output['text'] = bestText
				output['binSer'] = binarySeries
				output['stt'] = binz.getResultCompleteTT(myIteration, allKeys)
				if argumentsValues['verbose'] >= 2: 
					toPrintLev2 = argumentsValues['output']
					for tp in toPrintLev2:
						if tp in output:
							print output[tp]
	print "Reached in ",xyz," iterations"				
	return convergence			



def findOne_BESTFULLFITSolution(maxIters, goodScore, output, binarySeries=None, lMethod='BESTFIT'):
	convergence = []
	#for xyz in range(maxIters):
	xyz = 0
	bMethod = argumentsValues['bin-method']
	if bMethod > 0:
		clusters = int(math.pow(2,bMethod))
	bf = BestFit()
	clusters = int(math.pow(2,argumentsValues['bin-method']))

	while (output['score'] > goodScore or output['score'] == None):
		if xyz >= maxIters:
			break
		xyz +=1
		if output['score'] != None and output['score'] <= goodScore:
			if argumentsValues['verbose'] >= 1:
				print "STOP since reached score of "+str(goodScore)+" in "+str(xyz) + " iterations"
			break
		if argumentsValues['verbose'] >= 1 and xyz % 100 == 0: 
			print "ITERATIONS "+str(xyz)
			print output['score']
			print output['text']

		BSeries = []
		for o in allOSeries:
			if bMethod > 0:
				BSeries.append(binz.decrementalKMeanBinarization(dict(o), clusters, argumentsValues['reduction']))

		order = sorted(BSeries[0].keys())
		orderString = ''.join(order)
	
		k = 1
		p = itertools.combinations(orderString, 1)
		colCombinations1 = ["".join(p1) for p1 in p]
		answers1, error1 = bf.getBestFitAndError(k, colCombinations1, BSeries, order)

		k = 2
		p = itertools.combinations(orderString, 2)
		colCombinations2 = ["".join(p1) for p1 in p]		
		answers2, error2 = bf.getBestFitAndError(k, colCombinations2, BSeries, order)

		k = 3
		p = itertools.combinations(orderString, 3)
		colCombinations3 = ["".join(p1) for p1 in p]
		answers3, error3 = bf.getBestFitAndError(k, colCombinations3, BSeries, order)


		bestsFunc = {}
		bestsScore = {}
		for o in order:
			bestsFunc[o] = []
			bestsScore[o] = 10000

		if lMethod == 'BESTFIT':
			bestsFunc, bestsScore = bf.inferBestFunc(order,error1,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferBestFunc(order,error2,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferBestFunc(order,error3,bestsFunc,bestsScore)
		else:
			bestsFunc, bestsScore = bf.inferFullFunc(order,error1,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferFullFunc(order,error2,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferFullFunc(order,error3,bestsFunc,bestsScore)
		

		# clean up those that are longer but have score as the shortest ones
		for k, item in bestsFunc.items():
			if len(item) > 0:
				shortest = len(min(item, key=len))
				newList = []
				for i in item:
					if len(i) == shortest:
						newList.append(i)
				bestsFunc[k] = newList

		'''get the initial state for this division'''
		allIStates = []
		for b in BSeries:
			initialState = {}
			for k in order:
				initialState[k] = bool(b[k][0])
			allIStates.append(initialState)
		'''execute binary using the transition table'''
		textHeader = ""
		for i in order:
			textHeader += i + " = " + str(initialState[i]) + "\n"

		bestText = ''
		bestScore = 10000
		texts = bf.getText(bestsFunc, order, answers1, answers2, answers3, textHeader)

		for text in texts:
			sums = {}
			for k in order:
				sums[k] = 0
			for b in BSeries:
				header = ''
				for i in order:
					header += i + " = " + str(allIStates[BSeries.index(b)][i]) + "\n"
				textSim = header + text
				model = Model( mode='sync', text=textSim )
				
				length = len(b[order[0]])
				model.initialize()
				model.iterate( steps=length-1 )
				count = 0
				#compare the binary series
				
				for d in model.states:
					for k in d.keys():
						sums[k] += abs(b[k][count] - int(d[k]))
					count += 1
			score = 0
			for s,v in sums.items():
				score += v
			score /= (float(len(binarySeries[binarySeries.keys()[0]])) * float(len(sums)))
			if score < bestScore:
				bestScore = score
				bestText = textSim

		convergence.append(bestScore)
		if output['score'] is None or bestScore < output['score']:
			#print score
			#print text
			output['score'] = bestScore
			output['text'] = bestText
			output['binSer'] = binarySeries
			#output['stt'] = binz.getResultCompleteTT(myIteration, order)
			if argumentsValues['verbose'] >= 2: 
				toPrintLev2 = argumentsValues['output']
				for tp in toPrintLev2:
					if tp in output:
						print output[tp]
	print "Reached in ",xyz," iterations"
	return convergence


if __name__ == "__main__":
	main()
