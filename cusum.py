import pandas as pd
import numpy as np

data = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv") 
data = data.iloc[:,:-1]
data = np.array(data)
#CUSUM

#constants
m = 20
kpos = kneg = 10
thpos = thneg = 30

P = np.zeros(len(data[0]))	#positive changes
N = np.zeros(len(data[0]))	#negative changes
s = np.zeros((len(data), len(data[0])))

for t in range(0,len(data)):
	for col in range(0,len(data[0])):
		spos = 0	#positive signal
		sneg = 0	#negative signal
		P[col] = max(0, data[t,col] - (m+kpos) + P[col])
		N[col] = min(0, data[t,col] - (m-kneg) + N[col])

		if (P[col] > thpos):
			spos = 1
			P[col] = N[col] = 0
		if (N[col] < -thneg):
			sneg = 1
			P[col] = N[col] = 0
		s[t,col] = spos or sneg
		# print(spos or sneg)
np.savetxt('cusumEventVector.csv', s, fmt='%d', delimiter=',')