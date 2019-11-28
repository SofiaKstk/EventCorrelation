import pandas as pd
import numpy as np
import math

data = pd.read_csv("DATASET_CMA_CGM_NERVAL_5min.csv") 
data = np.array(data)
#print(data[:10,:])

#constants
k = 1

xprev = np.zeros(len(data[0]))
sprev = np.zeros(len(data[0]))
xcurr = np.zeros(len(data[0]))
scurr = np.zeros(len(data[0]))
s = np.zeros(len(data[0]))

for t in range(0,len(data)-1):
	for col in range(0,len(data[0])-1):
		xcurr[col] = xprev[col] + (data[t,col]-xprev[col])/(t+1)
		scurr[col] = math.sqrt( (1/(t+1)) * (t*(sprev[col]**2) + (data[t,col]-xcurr[col])*(data[t,col]-xprev[col]) ))
		
		UCL = xcurr[col] + k*scurr[col]
		LCL = xcurr[col] - k*scurr[col]
		
		if ((data[t,col] > UCL) or (data[t,col] < LCL)):
			s[col] = 1
		else:
			s[col] = 0
		xprev[col] = xcurr[col]
		sprev[col] = scurr[col]
	print(s)
	if(t == 16):
		break