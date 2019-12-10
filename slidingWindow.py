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

graph = {}

def updateGraph(prevPowSet, vertex, powerSet):
	if vertex not in graph:
		graph[vertex] = {}

	#CONNECT VERTEX WITH PREVIOUS EVENT
	for i in prevPowSet:
		key = streams(i).bits()
		if vertex not in graph[key]:
			graph[key][vertex] = 0			#CHANGE 0, 1 s
		graph[key][vertex] += 1

	#CONNECT VERTEX WITH THE REST OF THE EVENT'S VERTICES
	for j in powerSet:
		key = streams(j).bits()
		if key not in graph[vertex]:
			graph[vertex][key] = 0
		graph[vertex][key] += 1
		if key not in graph:
			graph[key] = {}
		if vertex not in graph[key]:
			graph[key][vertex] = 0
		graph[key][vertex] += 1


#GET COLUMN NAMES OF ALL STREAMS
columns = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv",  nrows = 0)
columns = tuple(columns.iloc[:,:-11])
streams = bitset('streams', columns)

#GET BINARY STREAMS
events = pd.read_csv("eventVector.csv", header=None)
events = events.iloc[:,:-10]
events = np.array(events)
train = events[:3]
test = events[2000:]

#NOTE TO SELF: update when all streams included!!!!
prevPowSet = []		
for ev in train:
	event = ''.join(map(str,ev))
	# print(event)
	selected = streams.frombits(event)
	# print(selected)
	ps = powerset(list(selected.members()))


	#skip empty set of powerset for non empty stream
	if len(ps) != 1:
		ps = ps[1:]
	print(len(ps))
	for i in range(0, len(ps)):
		#add every vertex that should exist inside the graph
		vertex = streams(ps[i]).bits()
		# print(vertex)
		updateGraph(prevPowSet, vertex, ps[i+1:])

	prevPowSet = ps

print(graph['0000000000000000100'])

