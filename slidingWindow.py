import random
import pandas as pd
import numpy as np
from bitsets import bitset 
from itertools import chain, combinations

def powerset(lst):
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    return result

# def updateGraph(prevPowSet, vertex, powerSet):
# 	if vertex not in graph:
# 		graph[vertex] = {}

# 	#CONNECT VERTEX WITH PREVIOUS EVENT
# 	for i in prevPowSet:
# 		key = streams(i).bits()
# 		if vertex not in graph[key]:
# 			graph[key][vertex] = 0			#CHANGE 0, 1 s
# 		graph[key][vertex] += 1

# 	#CONNECT VERTEX WITH THE REST OF THE EVENT'S VERTICES
# 	for j in powerSet:
# 		key = streams(j).bits()
# 		if key not in graph[vertex]:
# 			graph[vertex][key] = 0
# 		graph[vertex][key] += 1
# 		if key not in graph:
# 			graph[key] = {}
# 		if vertex not in graph[key]:
# 			graph[key][vertex] = 0
# 		graph[key][vertex] += 1

#GET COLUMN NAMES OF ALL STREAMS
columns = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv",  nrows = 0)
columns = tuple(columns.iloc[:,:-1])
streams = bitset('streams', columns)




#GET BINARY STREAMS
# vectors = pd.read_csv("cusumEventVector.csv", header=None)
vectors = pd.read_csv("shewhartEventVector.csv", header=None)

#KEEP K FIXED EVENTS FOR EACH EVENT VECTOR
k = 5



vectors = np.array(vectors)
events = []


for j in vectors:
	event = ''.join(map(str,j))
	ones = [n for n in range(0,len(event)) if event.find('1', n) == n]		#list of position of ones
	if len(ones)>k:
		rem = random.sample(ones,k=k)
		event = list(event)
		for i in list(set(ones) - set(rem)):
			event[i] = '0'
		event = ''.join(event)
	events.append(event)


w = 5
prevPSets = []
prevKeys = []
	

for i in range(0,w-1):
	selected = streams.frombits(events[i])
	pSet = powerset(list(selected.members()))
	if len(pSet) != 1:
		pSet = pSet[1:]
	prevPSets.append(pSet)
	prevKeys.append(events[i])

prediction = (None, 0)
exact = 0
numOfPreds = 0

for event in events[w-1:]:

	if prediction[0] == event:
		exact += 1
	prediction = (None, 0)


	selected = streams.frombits(event)
	currPS = powerset(list(selected.members()))

	if len(currPS) != 1:
		currPS = currPS[1:]
	prevPSets.append(currPS)
	prevKeys.append(event)

	powerList = []
	powerList = list(set([tuple(item) for sublist in prevPSets for item in sublist]))

	for k in range(0,len(powerList)):

		item = list(powerList[k])
		for l in range(k+1,len(powerList)):
			
			psItem = list(powerList[l])
			if item == psItem:
				continue
			
			i = 0
			while item not in prevPSets[i]:				#moves forward until first current encounter
				i += 1
			
			counter = psItemCount = idealCount = 0
			for j in range(i, w):
				# arithmitis
				if psItem in prevPSets[j]:
					counter += 1
					psItemCount += counter
				# paronomastis
				if item in prevPSets[j]:
					idealCount += (w-j)
			prob = psItemCount/idealCount
			# print(" prob "+str(prob))
			if prob > prediction[1] and prob > (1/w):
				prediction = (psItem, prob)
		
	prediction = (streams(prediction[0]).bits(), prediction[1])
	numOfPreds += 1
	print(event+" "+str(prediction[0])+" "+str(prediction[1]))

	prevKeys.pop(0)
	prevPSets.pop(0)
print(exact/numOfPreds)		

