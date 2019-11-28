import pandas as pd

data = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv") 

#CUSUM

x = data["DISPANCESLR"]

#constants
m = 13
kpos = kneg = 6
thpos = thneg = 30

P = 0	#positive changes
N = 0	#negative changes
t = 0	#time

while (1):
	spos = 0	#positive signal
	sneg = 0	#negative signal
	P = max(0, x[t] - (m+kpos) + P)
	N = min(0, x[t] - (m-kneg) + N)

	if (P > thpos):
		spos = 1
		P = N = 0
	if (N < -thneg):
		sneg = 1
		P = N = 0
	t += 1
	
	print(spos or sneg)
	if (t == 19):
		break	