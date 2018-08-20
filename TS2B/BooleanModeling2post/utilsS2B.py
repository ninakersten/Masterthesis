"""utilsS2B.py: Description of what foobar does."""
__author__      = "Natalie Berestovsky, Rice University"


from bitarray import bitarray
import random, itertools, numpy, Pycluster, math,sys
import scipy.special as func
from numpy import arange
debug = False

class Binarization(object):	
	
	'''
	reduces the binary series by removing redundant states and non-determanism (step 2 in paper)
	'''
	def reduceBinarySeries(self,binarySeries):
		reduced = {}
		stateCount = len(binarySeries[binarySeries.keys()[0]])
		same = True
		for i in binarySeries:
			reduced[i] = bitarray()
			if binarySeries[i][0] == True:
				reduced[i].append(True)
			else:
				reduced[i].append(False)
				
		for sc in range(1,stateCount):
			same = True
			for i,j in binarySeries.items():
				if j[sc] != j[sc-1]:
					same = False
					break
			if not same:
				for i,j in binarySeries.items():
					if j[sc] == True:
						reduced[i].append(True)
					else:
						reduced[i].append(False)
		# include last to capture the steady state
		for i,j in binarySeries.items():
			if j[stateCount-1] == True:
				reduced[i].append(True)
			else:
				reduced[i].append(False)
		
		return reduced

	'''implementation of the algorithm from <inference of boolean networks 
	from time series data with realistic characterisic> by Erkkila et al '''
	def reduceBinaryXOR(self, binarySeries):
		reduced = {}
		xors = []
		stateCount = len(binarySeries[binarySeries.keys()[0]])
		same = True

		# append first state
		for i in binarySeries:
			reduced[i] = bitarray()
			if binarySeries[i][0] == True:
				reduced[i].append(True)
			else:
				reduced[i].append(False)
		
		summ = 0
		matrix = binarySeries.values()
		for sc in range(1,stateCount):
			st1 = [row[sc-1] for row in matrix]
			st2 = [row[sc] for row in matrix]
			xor = [s1^s2 for s1,s2 in zip(st1,st2)]
			xors.append(xor)
			summ += xor.count(True)
		
		summ /= (stateCount-1)
		
		for sc in range(stateCount-1):
			st1 = [row[sc] for row in matrix]
			st2 = [row[sc+1] for row in matrix]
			if xors[sc].count(True) > summ:
				# add to the state changes
				for i,j in binarySeries.items():
					if j[sc+1] == True:
						reduced[i].append(True)
					else:
						reduced[i].append(False)
			
		return reduced
	
	def BASC_A_binarization(self, orig, reduction):
		print "BASC A binarization"
		#orig = {}
		#orig['A'] = [0.22,0.29,0.1,0.13,0.8,0.9,0.22,0.85,0.81,0.5]
		#orig['B'] = [0.5,0.57,0.1,0.13,0.8,0.9,0.5,0.85,0.81,0.58]
		
		binSeries = {}
		for k,seriesUnsorted in orig.items():
			if k == 'NON': continue
			C = []
			Ind = []
			costsDict = {}
			series = sorted(seriesUnsorted)
			series.insert(0,0)
			N = len(series)  # 10 species
			# pre-calc costs
			for i in range(1,N):
				#print "Calculating costs for ",i,"-th row"
				for j in range(1,N):
					cost = self.BASC_A_costFunction(series,i,j)
					costsDict[(i,j)] = cost
					#print cost,
				#print ''
			#print "Done pre-calculating costs"
			for i in range(N):
				C.append(['*']*(N))
				Ind.append(['*']*(N))
			
			#print "Starting to binarize:",k,N, series
			# Algorithm 1
			# Initialization
			for i in range(1,N):
				C[i][0] = costsDict[(i,N-1)]
			# Iterations
			for j in range(1,N-2):
				for i in range(1,N-j):
					scores = [sys.maxint]*N
					for d in range(i,N-j):
						cost = costsDict[(i,d)]
						#print 'cost func',i,d,' = ',cost,
						res = cost + C[d+1][j-1]
						scores[d] = res
						#print i, scores
						#print 'plus ',C[d][j-1],' is ',res
					C[i][j] = min(scores)
					Ind[i][j] = scores.index(C[i][j])
					#for c in C:
					#	print c
					#print 'chose',C[i][j], Ind[i][j]
				#if j % 10 == 0:
				#	print 'Dynamic programming - done with col',j,'out of ',(N-2)
			
			#print "Calculating optimizal breakpoints"
			P = []
			for i in range(N):
				P.append(['*']*N)
			# compute breakpoints now - Algorithm 2
			for j in range(1, N-2):
				z = j
				P[1][j] = Ind[1][z]
				if j > 1:
					z = z - 1
					for i in range(2,j+1):
						P[i][j] = Ind[P[i-1][j]+1][z]
						z = z - 1
			#for ip,p in enumerate(P):
			#	print p
			
			#print "Finding strongest discontinuities"
			# strongest discontinuity step
			v = []
			for j in range(1,N-2):
				maxQ = -1
				maxQid = -1
				for i in range(1,j+1):
					h,e = 0,0
					h = self.BASC_A_jumpSize(series,P,i,j,N-1)
					e = self.BASC_A_approxError(series, P, i,j, N-1)
					q = h / e
					if q > maxQ:
						maxQ = q
						maxQid = P[i][j]
					#print P[i][j], '(',e,h,')',
				v.append(maxQid)
				#print ' '
			#print 'v = ',v
			
			v_sorted = sorted(v)
			
			#binarization threshold
			totalElem = len(v)
			if totalElem % 2 == 0:
				medianIdx = totalElem/2 -1
			else:
				medianIdx = totalElem/2
			
			median = v_sorted[medianIdx]
			t = float(series[median + 1] + series[median]) / 2
			#print 'threshold = ',t
			
			binVals = bitarray()
			for i in seriesUnsorted:
				if i > t:
					binVals.append(True)
				else:
					binVals.append(False)
			binSeries[k] = binVals

		if reduction == 0:
			reduced = self.reduceBinarySeries(binSeries)
			return reduced
		if reduction == 1:
			reduced = self.reduceBinaryXOR(binSeries)
		return binSeries	
		
				
	def BASC_A_jumpSize(self,series, P,i,j,N):
		#0print series,i,j, '|',P[i][j], P[i-1][j], P[i+1][j],'#',
		res = None
		if i == 1 and j > 1:
			res = self.BASC_A_yFunc(series,P[i][j] + 1, P[i+1][j]) - self.BASC_A_yFunc(series, 1, P[i][j])
		elif i == j and j > 1:
			res = self.BASC_A_yFunc(series,P[i][j] + 1 , N) - self.BASC_A_yFunc(series, P[i-1][j] + 1, P[i][j])
		elif i == j and j == 1:
			res = self.BASC_A_yFunc(series,P[i][j] + 1,N) - self.BASC_A_yFunc(series, 1, P[i][j])
		else:
			res = self.BASC_A_yFunc(series,P[i][j] + 1 , P[i+1][j]) - self.BASC_A_yFunc(series, P[i-1][j] + 1, P[i][j])
		
		return res
		#return math.fabs(res)
		
	def BASC_A_approxError(self, series, P, i,j, N):
		z = float(series[P[i][j]] + series[P[i][j] + 1]) / 2
		err = 0
		for d in range (1,N+1):
			err += math.pow((series[d] - z),2)
		return err
			
			
	def BASC_A_costFunction(self, f,a,b):
		# sum [i from a to b] of (f(i) - y(a,b))^2
		score = 0
		for i in range(a,b+1):
			y_ab = self.BASC_A_yFunc(f,a,b)
			score += math.pow((f[i] - y_ab), 2)
		return score
			
	def BASC_A_yFunc(self,f,a,b):
		y_ab = 0
		# y (a,b) = sum [i from a to b] of (f(i) / (b-a+1))
		denom = (b - a + 1)
		for j in range (a,b+1):
			y_ab += f[j] / denom
		return y_ab
			


	def decrementalKMeanBinarization(self, orig, clusters, reduction):
		clusterData = {}
		clusterRes = {}
		binSeries = {}
		if clusters < 2:
			return None
		while clusters >= 2:
			for k,v in orig.items():
				if k == "NON":
					continue
				data = []
				for i in range(len(v)):
					row = [i,v[i]]
					data.append(row)
				x = numpy.vstack(v)
				clusterData[k] = x

				idx, error, nfound = Pycluster.kcluster(x, nclusters=clusters, method='a', dist='e')
				clusterRes[k] = (idx, error, nfound)

			# replace the values with the averages of the clusters
			for k,r in clusterRes.items():
				colors = []
				idx, error, nfound = r
				y = clusterData[k]
				x = numpy.arange(len(y))
				sizes = {}
				sums = {}
				for i in range(clusters):
					sizes[i] = 0
					sums[i] = 0
				for i in range(len(idx)):
					sizes[idx[i]] += 1
					sums[idx[i]] += y[i]
				# culculate sums
				for i in sums.keys():
					sums[i] /= sizes[i]
				# replace all the values with sums in the clusters
				averaged = []
				for i in idx:
					averaged.append(sums[i][0])
				orig[k] = averaged

			clusters /= 2
		# replace data with 0 and 1
		for k,v in orig.items():
			if k == "NON":
				continue
			mi = min(v)
			binVals = bitarray()
			for i in v:
				if i == mi:
					binVals.append(False)
				else:
					binVals.append(True)
			binSeries[k] = binVals
		# reduce binary series
		if reduction == 0:
			reduced = self.reduceBinarySeries(binSeries)
			return reduced
		if reduction == 1:
			reduced = self.reduceBinaryXOR(binSeries)
		return binSeries

		
	'''
	creates deterministic state transition table
	'''
	def stateTTMostFreq(self, ser):
		keys = sorted(ser[0].keys())
		if len(keys) == 0:
			return {}
		if not isinstance(ser[0][keys[0]], bitarray):
			raise TypeError("stateTTMostFreq functin takes dictionary of bitarrays")
		inouts = {}
		
		# create all possible input state combinations of 1s and 0s
		p = itertools.product("01", repeat=len(keys))
		for p1 in p:
			per = "".join(p1)
			inouts[per] = []
		
		# create first input input state string
		for s in ser:
			l = len(s[keys[0]])
			myinput = ""
			for k in keys:
				myinput += str(int(s[k][0]))
		
			# examine each output starting from 1 to the end
			for i in range(1,l):
				val = ""
				for k in keys:
					val += str(int(s[k][i]))
				inouts[myinput].append(val)
				myinput = val
		
		allFreq = {}
		for i,j in inouts.items():
			# reduce it - no output exists for this input
			if len(j) == 0:
				del(inouts[i])
			else:
				findMostFrequent = {}
				# get rid of undetermanism
				for j1 in j:
					if j1 in findMostFrequent:
						findMostFrequent[j1] += 1
					else:
						findMostFrequent[j1] = 1
				allFreq[i] = findMostFrequent
				e = findMostFrequent.keys()
				e.sort(cmp=lambda a,b: cmp(findMostFrequent[a],findMostFrequent[b]))

				if debug:
					print "State transition from the binarized time series"	
					print i, findMostFrequent
				
				highestScore = findMostFrequent[e[-1]]
				allHighest = []
				for indx in range(len(e)):
					if findMostFrequent[e[indx]] == highestScore:
						allHighest.append(e[indx])
				if len(allHighest) > 1:
					ran = random.randint(0, len(allHighest)-1)
					inouts[i] = [allHighest[ran]]
				else:
					inouts[i] = [e[-1]]

		return keys,allFreq,[inouts]	
		
	'''
	creates deterministic state transition table
	'''
	def stateTTMostFreqAllComb(self, ser):
		keys = sorted(ser[0].keys())
		if len(keys) == 0:
			return {}
		if not isinstance(ser[0][keys[0]], bitarray):
			raise TypeError("stateTTMostFreq functin takes dictionary of bitarrays")
		inouts = {}

		# create all possible input state combinations of 1s and 0s
		p = itertools.product("01", repeat=len(keys))
		for p1 in p:
			per = "".join(p1)
			inouts[per] = []

		# create first input input state string
		for s in ser:
			l = len(s[keys[0]])
			myinput = ""
			for k in keys:
				myinput += str(int(s[k][0]))

			# examine each output starting from 1 to the end
			for i in range(1,l):
				val = ""
				for k in keys:
					val += str(int(s[k][i]))
				inouts[myinput].append(val)
				myinput = val

		allFreq = {}
		for i,j in inouts.items():
			# reduce it - no output exists for this input
			if len(j) == 0:
				del(inouts[i])
			else:
				findMostFrequent = {}
				# get rid of undetermanism
				for j1 in j:
					if j1 in findMostFrequent:
						findMostFrequent[j1] += 1
					else:
						findMostFrequent[j1] = 1

				
				allFreq[i] = findMostFrequent
				if debug:
					print "State transition from the binarized time series"	
					print i, findMostFrequent

		rInOuts = {}
		combNum = 1
		allTansitionTables = []
		for i,findMostFrequent in allFreq.items():
			if len(findMostFrequent) == 1:
				rInOuts[i] = [findMostFrequent.keys()[0]]
				del(allFreq[i])
			else:
				combNum *= len(findMostFrequent)
		for i in range(combNum):
			allTansitionTables.append(dict(rInOuts))
		#print allTansitionTables[0]
		for i,findMostFrequent in allFreq.items():
			for idx in range(combNum):
				#print len(findMostFrequent), idx % len(findMostFrequent), i, findMostFrequent, findMostFrequent.keys()[idx % len(findMostFrequent)]
				allTansitionTables[idx][i] = [findMostFrequent.keys()[idx % len(findMostFrequent)]]
		return keys,allTansitionTables
		
	'''FOR FREQ. Version'''
	def stateTTMostFreq2(self, ser):
		keys = sorted(ser[0].keys())
		if len(keys) == 0:
			return {}
		if not isinstance(ser[0][keys[0]], bitarray):
			raise TypeError("stateTTMostFreq functin takes dictionary of bitarrays")
		inouts = {}

		# create all possible input state combinations of 1s and 0s
		p = itertools.product("01", repeat=len(keys))
		for p1 in p:
			per = "".join(p1)
			inouts[per] = []

		# create first input input state string
		for s in ser:
			l = len(s[keys[0]])
			myinput = ""
			for k in keys:
				myinput += str(int(s[k][0]))

			# examine each output starting from 1 to the end
			for i in range(1,l):
				val = ""
				for k in keys:
					val += str(int(s[k][i]))
				inouts[myinput].append(val)
				myinput = val
		
		allMostFrequent = {}
		maxcount = 0
		for i,j in inouts.items():
			# reduce it - no output exists for this input
			if len(j) == 0:
				del(inouts[i])
			else:
				findMostFrequent = {}
				# get rid of undetermanism
				for j1 in j:
					if j1 in findMostFrequent:
						findMostFrequent[j1] += 1
					else:
						findMostFrequent[j1] = 1
				print i,findMostFrequent
				# find 100 percent
				for f,c in findMostFrequent.items():
					if c > maxcount:
						maxcount = c
					
				allMostFrequent[i] = findMostFrequent
				
		print maxcount
		for i,allcases in allMostFrequent.items():
			mc = 0
			ml = allcases.keys()[0]
			for k,onecase in allcases.items():
				if onecase > mc:
					mc = onecase
					ml = k
			# if > 30% keep, otherwise del
			if (mc * 1.0) / maxcount > 0.3:
				inouts[i] = [ml]
			else:
				del(inouts[i])	
		return keys,inouts
	
	'''
	creates complete Transition table function for a set of (non-deterministic) inputs and output
	'''
	def getTTFunction(self, inps, outp, tt, keys):
		finalTable = {}
		iidx = keys.index(outp)
		for bin in range(2):
			finalTable[bin] = []
			# since item is output, we are seeing if it has the right value in the OUTPUTS, not keys
			consideredIns = []
			for k in tt.keys():
				for kk in tt[k]:
					if int(kk[iidx]) == bin:
						consideredIns.append(k)

			p = itertools.product("01", repeat=len(inps))
			for p1 in p:
				finalList = list(consideredIns)
				#print p1, finalOuts
				for k in consideredIns:
					# that is done by matching the idx
					for idx in range(len(inps)):
						character = inps[idx]
						value = p1[idx]
						position = keys.index(character)
						#print character, value, position, int(k[position]), k
						if int(k[position]) != int(value):
							finalList.remove(k)
							break
				#for each item, remove unrelated indexes and get rid of repetivie inputs
				#cleanFinalList = []
				for l in range(len(finalList)):
					redo = ""
					for letter in inps:
						redo += finalList[l][keys.index(letter)]
					finalList[l] = redo
					if redo not in finalTable[bin]:
						finalTable[bin].append(redo)
		return finalTable

	'''
	creates a complete state transition table (only is done if the user wants it in the output)
	'''
	def getResultCompleteTT(self, data, allKeys):
		if len(allKeys) == 0:
			return {}
		inouts = {}
		
		# create all possible input state combinations of 1s and 0s
		p = itertools.product("01", repeat=len(allKeys))
		for p1 in p:
			per = "".join(p1)
			next = list([])
			for s in range(len(allKeys)):
				species = allKeys[s]
				#set it to my old value then search for funciton and reset if it exists
				next.append(str(p1[s]))
				for io,func in data.items():
					if io.startswith(species):
						curInput = ""
						#found my input
						o,i = io.split('\'')
						for ii in i:
							inputIdx = allKeys.index(ii)
							curInput += p1[inputIdx]
						
						if curInput in func[0]:
							next[s] = '0'
						else:
							next[s] = '1'

			next = "".join(next)
				
						 
							
			inouts[per] = next
				
		return inouts
		
	

class KarnaughMaps(object):	
	
	global items
	global i
	
	def __init__(self):
		self.i = 0
		self.items = []
	
	def getFunction1(self, name, func):
		o,self.i = name.split("\'")
		if len(self.i) != 1:
			return ""
		f = ""
		if len(func[0]) == 0:
			#f = o+"* = "+self.i + " or not "+self.i
			f = ""
		elif len(func[1]) == 0:
			#f = o+"* = "+self.i + " and not "+self.i
			f = ""
		elif func[0][0] == '0' and func[1][0] == '1':
			f = o+"* = "+self.i
		elif func[0][0] == '1' and func[1][0] == '0':
			f = o+"* = not "+self.i
		return f
	
	def getFunction2(self, name, func):
		o,self.i = name.split("\'")
		if len(self.i) != 2:
			return ""
		f = o+"* = "
		table = [[0,0],[0,0]]
		for res,inputs in func.items():
			for inp in inputs:
				table[int(inp[0])][int(inp[1])] = res
		
		self.items = []
		if (table[0][0] + table[1][0]) == 2:
			self.items.append("not "+self.i[1])
		if (table[0][1] + table[1][1]) == 2:
			self.items.append(self.i[1])
		if (table[0][0] + table[0][1]) == 2:
			self.items.append("not "+self.i[0])
		if (table[1][0] + table[1][1]) == 2:
			self.items.append(self.i[0])
		
		#check if we have OR relationships, if not, it's an AND, find it
		if len(self.items) == 0:
			if table[0][0] == 1:
				self.items.append("not "+self.i[0]+" and not "+self.i[1])
			if table[0][1] == 1:
				self.items.append("not "+self.i[0]+" and "+self.i[1])
			if table[1][0] == 1:
				self.items.append(self.i[0]+" and not "+self.i[1])
			if table[1][1] == 1:
				self.items.append(self.i[0]+" and "+self.i[1])
		
		if len(self.items) <= 0:
			return ""			
		f += self.items[0]
		for inum in range(1,len(self.items)):
			f += " or "+self.items[inum]
		return f
		
	
	def getFunction3(self, name, func):
		bin2int = ['00','01','10','11']
		o,self.i = name.split("\'")
		if len(self.i) != 3:
			return ""
		f = o+"* = "
		table = [[0,0,0,0],[0,0,0,0]]
		for res,inputs in func.items():
			for inp in inputs:
				table[int(inp[0])][bin2int.index(inp[1:])] = res
		self.items = []
		
		## add these and then remove then if find something bigger
		if table[0][0] == 1:
			self.items.append("not "+self.i[0]+" and not "+self.i[1]+" and not "+self.i[2])
		if table[0][1] == 1:
			self.items.append("not "+self.i[0]+" and not "+self.i[1]+" and "+self.i[2])
		if table[0][2] == 1:
			self.items.append("not "+self.i[0]+" and "+self.i[1]+" and not "+self.i[2])
		if table[0][3] == 1:
			self.items.append("not "+self.i[0]+" and "+self.i[1]+" and "+self.i[2])
		if table[1][0] == 1:
			self.items.append(self.i[0]+" and not "+self.i[1]+" and not "+self.i[2])
		if table[1][1] == 1:
			self.items.append(self.i[0]+" and not "+self.i[1]+" and "+self.i[2])
		if table[1][2] == 1:
			self.items.append(self.i[0]+" and "+self.i[1]+" and not "+self.i[2])
		if table[1][3] == 1:
			self.items.append(self.i[0]+" and "+self.i[1]+" and "+self.i[2])
		
		
		# possibility of the whole value
		if sum(table[0]) == 4:
			self.items.append("not "+self.i[0])
			self.__removeSingles(0,0)
			self.__removeSingles(0,1)
			self.__removeSingles(0,2)
			self.__removeSingles(0,3)
		if sum(table[1]) == 4:
			self.items.append(self.i[0])
			self.__removeSingles(1,0)
			self.__removeSingles(1,1)
			self.__removeSingles(1,2)
			self.__removeSingles(1,3)
		if (sum(table[0][:2]) + sum(table[1][:2])) == 4:
			self.items.append("not "+self.i[1])
			self.__removeSingles(0,0)
			self.__removeSingles(0,1)
			self.__removeSingles(1,0)
			self.__removeSingles(1,1)
		if (sum(table[0][2:]) + sum(table[1][2:])) == 4:
			self.items.append(self.i[1])
			self.__removeSingles(0,2)
			self.__removeSingles(0,3)
			self.__removeSingles(1,2)
			self.__removeSingles(1,3)
			
		# can check for all double witouth A here since only singles have already been checked
		if (table[0][0] + table[0][2] + table[1][0] + table[1][2]) == 4:
			self.items.append("not "+self.i[2])
			self.__removeSingles(0,0)
			self.__removeSingles(0,2)
			self.__removeSingles(1,0)
			self.__removeSingles(1,2)
		if (table[0][1] + table[0][3] + table[1][1] + table[1][3]) == 4:
			self.items.append(self.i[2])
			self.__removeSingles(0,1)
			self.__removeSingles(0,3)
			self.__removeSingles(1,1)
			self.__removeSingles(1,3)
			
		# possibilities of doubles for A and B
		if sum(table[0][:2]) == 2 and ("not "+self.i[0] not in self.items) and ("not "+self.i[1] not in self.items):
			self.items.append("not "+self.i[0]+" and not "+self.i[1])
			self.__removeSingles(0,0)
			self.__removeSingles(0,1)
		if sum(table[0][2:]) == 2 and ("not "+self.i[0] not in self.items) and (self.i[1] not in self.items):
			self.items.append("not "+self.i[0]+" and "+self.i[1])
			self.__removeSingles(0,2)
			self.__removeSingles(0,3)
		if sum(table[1][:2]) == 2 and (self.i[0] not in self.items) and ("not "+self.i[1] not in self.items):
			self.items.append(self.i[0]+" and not "+self.i[1])
			self.__removeSingles(1,0)
			self.__removeSingles(1,1)
		if sum(table[1][2:]) == 2 and (self.i[0] not in self.items) and (self.i[1] not in self.items):
			self.items.append(self.i[0]+" and "+self.i[1])
			self.__removeSingles(1,2)
			self.__removeSingles(1,3)
		
		# possibilities of doubles for A and C
		if (table[0][0] + table[0][2]) == 2 and ("not "+self.i[0] not in self.items) and ("not "+self.i[2] not in self.items):
			self.items.append("not "+self.i[0]+" and not "+self.i[2])
			self.__removeSingles(0,0)
			self.__removeSingles(0,2)
		if (table[0][1] + table[0][3]) == 2 and ("not "+self.i[0] not in self.items) and (self.i[2] not in self.items):
			self.items.append("not "+self.i[0]+" and "+self.i[2])
			self.__removeSingles(0,1)
			self.__removeSingles(0,3)
		if (table[1][0] + table[1][2]) == 2 and (self.i[0] not in self.items) and ("not "+self.i[2] not in self.items):
			self.items.append(self.i[0]+" and not "+self.i[2])
			self.__removeSingles(1,0)
			self.__removeSingles(1,2)
		if (table[1][1] + table[1][3]) == 2 and (self.i[0] not in self.items) and (self.i[2] not in self.items):
			self.items.append(self.i[0]+" and "+self.i[2])
			self.__removeSingles(1,1)
			self.__removeSingles(1,3)
			
		# possibilities of doubles for B and C
		if (table[0][0] + table[1][0]) == 2 and ("not "+self.i[1] not in self.items) and ("not "+self.i[2] not in self.items):
			self.items.append("not "+self.i[1]+" and not "+self.i[2])
			self.__removeSingles(0,0)
			self.__removeSingles(1,0)
		if (table[0][1] + table[1][1]) == 2 and ("not "+self.i[1] not in self.items) and (self.i[2] not in self.items):
			self.items.append("not "+self.i[1]+" and "+self.i[2])
			self.__removeSingles(0,1)
			self.__removeSingles(1,1)
		if (table[0][2] + table[1][2]) == 2 and (self.i[1] not in self.items) and ("not "+self.i[2] not in self.items):
			self.items.append(self.i[1]+" and not "+self.i[2])
			self.__removeSingles(0,2)
			self.__removeSingles(1,2)
		if (table[0][3] + table[1][3]) == 2 and (self.i[1] not in self.items) and (self.i[2] not in self.items):
			self.items.append(self.i[1]+" and "+self.i[2])
			self.__removeSingles(0,3)
			self.__removeSingles(1,3)
			
		# if items is empty get all the triples
		
		if len(self.items) <= 0:
			return ""
		f += self.items[0]
		for inum in range(1,len(self.items)):
			f += " or "+self.items[inum]
		return f
				
	def __removeSingles(self,x,y):
		zerozero = "not "+self.i[0]+" and not "+self.i[1]+" and not "+self.i[2]
		zeroone = "not "+self.i[0]+" and not "+self.i[1]+" and "+self.i[2]
		zerotwo = "not "+self.i[0]+" and "+self.i[1]+" and not "+self.i[2]
		zerothree = "not "+self.i[0]+" and "+self.i[1]+" and "+self.i[2]
		onezero = self.i[0]+" and not "+self.i[1]+" and not "+self.i[2]
		oneone = self.i[0]+" and not "+self.i[1]+" and "+self.i[2]
		onetwo = self.i[0]+" and "+self.i[1]+" and not "+self.i[2]
		onethree = self.i[0]+" and "+self.i[1]+" and "+self.i[2]
		
		
		if x == 0 and y == 0 and zerozero in self.items:
			self.items.remove(zerozero)
		if x == 0 and y == 1 and zeroone in self.items:
			self.items.remove(zeroone)
		if x == 0 and y == 2 and zerotwo in self.items:
			self.items.remove(zerotwo)
		if x == 0 and y == 3 and zerothree in self.items:
			self.items.remove(zerothree)
		if x == 1 and y == 0 and onezero in self.items:
			self.items.remove(onezero)
		if x == 1 and y == 1 and oneone in self.items:
			self.items.remove(oneone)
		if x == 1 and y == 2 and onetwo in self.items:
			self.items.remove(onetwo)
		if x == 1 and y == 3 and onethree in self.items:
			self.items.remove(onethree)

		
class BestFit(object):

	global rowCombinations1
	global rowCombinations2
	global rowCombinations3

	
	def __init__(self):
		self.rowCombinations1 = ['0','1']
		self.rowCombinations2 = ['00','01','10','11',]
		self.rowCombinations3 = ['000','001','010','011','100','101','110','111']

		
		
	def getBestFitAndError(self, k, colCombinations, binarySeries, order):
		kk = int(math.pow(2,k))
		kkk = 2 * kk
		ni = len(order)
		
		answers = {} # keys are combinations; lists are the output of thisthis combination in rowCombination# order
		error = {}
		for c in colCombinations:
			optErr = []
			optF = []
			#This matrix (C01) has the role of c^(0) and c^(1) for all interesting genes. Further, C01 = [c^(0),c^(1)]
			C01 = []
			for o in order:
				C01.append([0] * kkk)
			for b in binarySeries:
				allSeries = [b[k] for k in order]
				seriesLength = len(b[b.keys()[0]])
				
				
				c_list = list(c)
				neededSeries = [b[k] for k in c_list] 
				for i in range(seriesLength-1):
					sampleIn = [str(int(ba[i])) for ba in neededSeries]
					sampleAllOut = [ba[i+1] for ba in allSeries]
					sampleInInt = ''.join(sampleIn)
					dn = int(sampleInInt,2)
					# take care of 0 part: C01(logical(1-Y(:,j)),dn) = C01(logical(1-Y(:,j)),dn) + w(j);
					zeroY = [int(not z) for z in sampleAllOut]
					for idx, val in enumerate(zeroY):
						C01[idx][dn] += val
					# take care of the 1 part: C01(logical(Y(:,j)),kk+dn) = C01(logical(Y(:,j)),kk+dn) + w(j);
					oneY = [int(z) for z in sampleAllOut]
					for idx, val in enumerate(oneY):
						C01[idx][dn+kk] += val
				# Find the Best-Fit function for all the nodes: [OptErr,OptF] = min(cat(3,C01(:,1:kk),C01(:,kk+1:end)),[],3);

			for idx in range(len(C01)):
				optErr.append([])
				optF.append([])
				for i in range(kk):
					if C01[idx][i] < C01[idx][i+kk]:
						optErr[idx].append(C01[idx][i])
						optF[idx].append(1)
					elif C01[idx][i] > C01[idx][i+kk]:
						optErr[idx].append(C01[idx][i+kk])
						optF[idx].append(0)
					else:
						optErr[idx].append(C01[idx][i])
						r = random.random()
						if r > 0.5:
							optF[idx].append(0)
						else:
							optF[idx].append(1)			
			
			# sum the error rows
			for i, oe in enumerate(optErr):
				sum_oe = sum(oe)
				optErr[i] = sum_oe
			
			#store
			answers[c] = optF
			error[c] = optErr
		
		return answers, error
		
	def inferBestFunc(self, order, error, bestsFunc, bestsScore):
		# go thru errors and find the mins
		for idx, val in enumerate(order):
			for comb, errors in error.items():
				if errors[idx] < bestsScore[val]:
					bestsFunc[val] = [comb]
					bestsScore[val] = errors[idx]
				elif errors[idx] == bestsScore[val]:
					bestsFunc[val].append(comb)
					
		return bestsFunc, bestsScore
	
	def inferFullFunc(self, order, error, bestsFunc, bestsScore):
		# go thru errors and find the mins
		for idx, val in enumerate(order):
			for comb, errors in error.items():
				#if errors[idx] < bestsScore[val]:
				if errors[idx] == 0:
					if val in bestsFunc:
						bestsFunc[val].append(comb)
					else:
						bestsFunc[val] = [comb]
						bestsScore[val] = errors[idx]

		return bestsFunc, bestsScore
	
	def getText(self, bestsFunc, order, answers1, answers2, answers3, header):
		text = str(header)
		km = KarnaughMaps()
		allTexts = {}
		texts2return = []
		
		for k, funcs in bestsFunc.items():
			idx = order.index(k)
			for f in funcs:
				name = k+'\''+f
				if len(f) == 1:
					myOutputs  = answers1[f][idx]
				elif len(f) == 2:
					myOutputs  = answers2[f][idx]
				else:
					myOutputs  = answers3[f][idx]
				myData = {0:[], 1:[]}
				if len(f) == 1:
					for i, comb in enumerate(self.rowCombinations1):
						if myOutputs[i] == 0:
							myData[0].append(comb)
						else:
							myData[1].append(comb)
				elif len(f) == 2:
					for i, comb in enumerate(self.rowCombinations2):
						if myOutputs[i] == 0:
							myData[0].append(comb)
						else:
							myData[1].append(comb)
				else:
					for i, comb in enumerate(self.rowCombinations3):
						if myOutputs[i] == 0:
							myData[0].append(comb)
						else:
							myData[1].append(comb)
			
				#print name, func
				if len(f) == 1:
					f = km.getFunction1(name, myData)
				elif len(f) == 2:
					f = km.getFunction2(name, myData)
				elif len(f) == 3:
					f = km.getFunction3(name, myData)
			
				if len(f) > 0:
					if k in allTexts:
						allTexts[k].append(f)
					else:
						allTexts[k] = [f]
		for zz in range(100):
			text = ''
			for k in allTexts.keys():
				rText = random.choice(allTexts[k])
				if rText != '':
					text += random.choice(allTexts[k]) +'\n'
			if text not in texts2return and text != '':
				texts2return.append(text)
		return texts2return
