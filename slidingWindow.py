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

# GET COLUMN NAMES OF ALL STREAMS
columns = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv",  nrows = 0)
columns = tuple(columns.iloc[:,:-1])
streams = bitset('streams', columns)

# GET k FIXED EVENT VECTORS
events = pd.read_csv("randomKevents.csv", header=None, squeeze=True)
events = np.array(events)

# CONSTANTS
w = 4		# w is the wide of our window

prevPSets = []
prevKeys = []
# PREPARE UP TO w-1 EVENT VECTORS
for i in range(0,w-1):
	selected = streams.frombits(events[i])
	pSet = []
	pSet = powerset(list(selected.members()))
	if len(pSet) != 1:
		pSet = pSet[1:]
	# get the powerset for each event vector and the key for predictions
	prevPSets.append(pSet)
	prevKeys.append(events[i])

prediction = (None, 0)
exact = 0
numOfPreds = 0
flag = 0
recallExact = 0

for event in events[w-1:]:

	# check if previous prediction was correct
	if prediction[0] != None:
		binPred = int(prediction[0], base=2)
		binEvent = int(event, base=2)
		bitand = '{0:029b}'.format(binPred & binEvent)
		if bitand == prediction[0]:
			exact += 1
			if int(bitand, base=2) <= binEvent:
				recallExact += 1

	prediction = (None, 0)



	# enter the current event to the table
	selected = streams.frombits(event)
	currPS = powerset(list(selected.members()))
	if len(currPS) != 1:
		currPS = currPS[1:]
	prevPSets.append(currPS)
	prevKeys.append(event)

	# get all sets in the powersets that have appeared in the time window
	powerList = []
	powerList = list(set([tuple(item) for sublist in prevPSets for item in sublist]))
	# print(powerList)
	# iterate for each couple of sets within the powerset list to get the one that has the maximum probability
	for k in range(0,len(powerList)):

		# the given set
		item = list(powerList[k])
		for l in range(k+1,len(powerList)):
			
			# the set that its probability is being calculated currently
			psItem = list(powerList[l])

			# start from the first encounter of the given set in the table
			i = 0
			while item not in prevPSets[i]:
				i += 1
			
			# from there onward, calculate the probability of the set
			psItemCount = idealCount = 0
			for j in range(i, w):
				# numerator
				# if psItem in prevPSets[j]:
					
				# denominator
				if item in prevPSets[j]:
					idealCount += (w-j)
					for m in range(j,w):
						if psItem in prevPSets[m]:
							psItemCount += 1
				# if flag ==2:
				# 	print(prevPSets[j])
				# 	print(str(psItemCount)+" / "+str(idealCount))
			prob = psItemCount/idealCount
			if prob>1:
				print("item1 "+str(item)+" item2 "+str(psItem)+" prob "+str(prob))
			# get the maximum probability of all combinations
			if prob > prediction[1] and prob > (1/w):
				prediction = (psItem, prob)
	if prediction[0] != None:
		prediction = (streams(prediction[0]).bits(), prediction[1])
		numOfPreds += 1

	# print(event+" "+str(prediction[0])+" "+str(prediction[1]))
	# remove the oldest entry
	prevKeys.pop(0)
	prevPSets.pop(0)

print(exact/numOfPreds)
print(recallExact/len(events[w-1:]))