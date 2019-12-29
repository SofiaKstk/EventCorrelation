import random
import pandas as pd
import numpy as np

# GET BINARY STREAMS
vectors = pd.read_csv("cusumEventVector.csv", header=None)
# vectors = pd.read_csv("shewhartEventVector.csv", header=None)
vectors = np.array(vectors)

for i in range(1,8):
	k = i		# k fixed events happening at any moment

	# KEEP RANDOM K FIXED EVENTS FOR EACH EVENT VECTOR
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
	file = 'cusumRandomKevents'+str(k)+'.csv'
	np.savetxt(file, events, fmt='%s', delimiter=',')