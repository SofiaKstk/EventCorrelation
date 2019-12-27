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
def main(k, w, p, steps, file, algorithm = "shewhart"):
	columns = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv",  nrows = 0)
	columns = tuple(columns.iloc[:,:-1])
	streams = bitset('streams', columns)

	# GET k FIXED EVENT VECTORS
	res = open(file, "w")
	res.write("SLIDING WINDOW,\tWINDOW LENGTH "+str(w)+",\tFIXED "+str(k)+",\tPROBABILITY GREATER THAN "+str(p)+",\t")	
	if k == 0:
		csvFile = algorithm + "EventVector.csv"
		res.write(algorithm+" ALGORITHM\n")
	else:
		csvFile = "randomKevents" + str(k) + ".csv"
	events = pd.read_csv(csvFile, header=None, squeeze=True)

	events = np.array(events)

	# CONSTANTS
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
	numOfPreds = 0

	f = open("predictions.csv", "w")

	entry = str(prevKeys[w-2])+" 0 0\n"
	f.write(entry)
	for event in events[w-1:]:

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
					if item in prevPSets[j]:
						idealCount += (w-j)
						for m in range(j,w):
							if psItem in prevPSets[m]:
								psItemCount += 1
				prob = psItemCount/idealCount
				if prob>1:
					print("item1 "+str(item)+" item2 "+str(psItem)+" prob "+str(prob))
				# get the maximum probability of all combinations
				if prob > prediction[1] and prob >= p:
					prediction = (psItem, prob)
		if prediction[0] != None:
			prediction = (streams(prediction[0]).bits(), prediction[1])
			numOfPreds += 1

		entry = str(event)+" "+str(prediction[0])+" "+str(prediction[1])+"\n"
		f.write(entry)
		# remove the oldest entry
		prevKeys.pop(0)
		prevPSets.pop(0)


	f.close()

	results = pd.read_csv("predictions.csv", delimiter=" ")
	results = np.array(results)
	res.write("PROBABILITY / TRUE/FALSE\n")

	exact = 0
	recallExact = 0
	for i in range(0,len(results)):
		pred = results[i,1]
		prob = results[i,2]
		flag = 0
		for j in range(1,steps+1):
			if i+j < len(results):
				event = results[i+j,0]

				# check if previous prediction was correct
				if pred != "None":
					binPred = int(pred, base=2)
					binEvent = int(event, base=2)
					bitand = '{0:029b}'.format(binPred & binEvent)
					if bitand == pred:
						exact += 1
						flag = 1
						if int(bitand, base=2) <= binEvent:
							recallExact += 1
						break
		
		res.write(str(prob)+" "+str(flag)+"\n")

	precision = exact/numOfPreds
	recall = recallExact/len(events[w-1:])
	print("Precision is: " + str(precision))
	res.write("Precision is: " + str(precision)+"\n")
	print("Recall is "+ str(recall))
	res.write("Recall is: " + str(recall)+"\n")

if __name__ == "__main__":
	main(5, 3, 0.1, 1, "sliding571.txt")
	# k,w,p,steps,file,algorithm