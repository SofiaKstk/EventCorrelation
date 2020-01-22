import random
import pandas as pd
import numpy as np
import sys
from bitsets import bitset 
from itertools import chain, combinations
from math import exp
from threading import Lock,get_ident
import os

mutex = Lock()

def powerset(lst):
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    return result

def linearAgeing(k, n, i):
	age = - 2*k*(i - 1)/(n - 1) + k + 1
	return age

def exponentialAgeing(k, n, i):
	age = exp(-k*i)
	return age

# GET COLUMN NAMES OF ALL STREAMS
def sliding(k, w, p, steps, ageingFunction, file, algorithm = "shewhart"):
	k = int(k)
	w = int(w)
	p = float(p)
	steps = int(steps)
	columns = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv",  nrows = 0)
	columns = tuple(columns.iloc[:,:-1])
	streams = bitset('streams', columns)

	# GET k FIXED EVENT VECTORS
	res = open(file, "w")
	res.write("SLIDING WINDOW,\tWINDOW LENGTH "+str(w)+",\tFIXED "+str(k)+",\tPROBABILITY GREATER THAN "+str(p)+",\t"+ algorithm+" ALGORITHM\n,\t"+ageingFunction+" ageing\t")	
	if k == 0:
		csvFile = algorithm + "EventVector.csv"
	else:
		csvFile = algorithm + "randomKevents" + str(k) + ".csv"
	events = pd.read_csv(csvFile, header=None, squeeze=True)
	events = np.array(events)

	if ageingFunction == "linear":
		ageingFun = linearAgeing
	else:
		ageingFun = exponentialAgeing

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

	f = open("predictions"+str(get_ident())+".csv", "w")

	entry = str(prevKeys[w-2])+" 0 0\n"
	f.write(entry)
	ageing = (None, 0, 0)
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

		# even if it doesn't predict anything, get from previous predictions
		if ageing[0] != None and ageing[1] > prediction[1]:
			prediction = (ageing[0], ageing[1])
			ageing = (ageing[0], ageing[1], 0)
		if numOfPreds > 2:
			ageing = (ageing[0], ageing[1]*ageingFun(0.3,numOfPreds-1, ageing[2]), ageing[2]+1)

		entry = str(event)+" "+str(prediction[0])+" "+str(prediction[1])+"\n"
		f.write(entry)
		# remove the oldest entry
		prevKeys.pop(0)
		prevPSets.pop(0)


	f.close()

	
	results = pd.read_csv("predictions"+str(get_ident())+".csv", delimiter=" ")
	results = np.array(results)
	res.write("PROBABILITY / TRUE/FALSE\n")

	exact = 0
	recallExact = 0
	for i in range(0,len(results)):
		pred = results[i,1]
		prob = results[i,2]
		flag = 0
		mutex.acquire()
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
		mutex.release()
		
		res.write(str(prob)+" "+str(flag)+"\n")

	if numOfPreds == 0:
		precision = 0
	else:
		precision = (exact/numOfPreds)*100
	recall = (recallExact/len(events[w-1:]))*100
	print("Precision is: " + str(precision) + "%")
	res.write("Precision is: " + str(precision) + "%\n")
	print("Recall is "+ str(recall) + "%")
	res.write("Recall is: " + str(recall) + "%\n")
	os.remove("predictions"+str(get_ident())+".csv")



if __name__ == "__main__":
	sliding(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
	# sliding(5,3,0.3,3,"linear","slid123456789.txt")
	# k,w,p,steps,ageing,file,algorithm