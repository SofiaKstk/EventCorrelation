import pandas as pd
import numpy as np

graph = {}
freq = {}

def updateFreq(event):
	if event not in freq:
		freq[event] = 0
	freq[event] += 1


def updateGraph(prevState, event):
	if event not in graph:
		graph[event] = {}

	if event not in graph[prevState]:
		graph[prevState][event] = 0
	graph[prevState][event] += 1

events = pd.read_csv("eventVector.csv", header=None)
events = np.array(events)
train = events[:2000]
test = events[2000:]

#FIRST VECTOR
event = ''.join(map(str,events[0]))
graph[event] = {}
freq[event] = 1


#TRAINING DATA
t = 0
for i in train[1:]:
	prevState = event
	event = ''.join(map(str,i))
	updateGraph(prevState, event)
	updateFreq(event)
	t += 1
	#probability = freq/t

#TESTING DATA
f = open("predictions.txt", "w")
f.write("PREDICTION\t\t/\t\tEVENT\n")

#FIRST PREDICTION
pred = max(graph[event], key=graph[event].get)

zer = 0
predictions = 0
precision = 0
exact = 0
for i in test:
	#NEW EVENT
	prevState = event
	event = ''.join(map(str,i))

	entry = str(pred) + " / " + str(event) + "\n"

	f.write(entry)

	#CHECK IF PREDICTION WAS CORRECT
	if pred:
		s1 = int(pred, base=2)
		s2 = int(event, base=2)
		bitand = '{0:029b}'.format(s1 & s2)
		if bitand == pred:
			precision+=1
			if s1 == s2:
				exact+=1

	#UPDATE GRAPH
	updateGraph(prevState, event)
	updateFreq(event)
	t += 1

	#CHECK IF ABLE TO MAKE PREDICTION
	#print(event)
	if graph[event]:
		pred = max(graph[event], key=graph[event].get)
		predictions+=1
	else:
		pred = None
	
	

print(precision/predictions)
print(exact/predictions)
print(predictions)