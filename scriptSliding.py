import os
import numpy as np


for k in range(1, 8):
	for w in range(3, 8):
		for p in np.arange(0.4, 1.0, 0.1):
			for step in [1, 2, 3]:
				file = "results/sliding/step" + str(k) + str(w) + str(step) + ".txt"
				print("slidingWindow.py " + str(k) + " " + str(w) + " " + str(step) + " " + file)
				os.system("slidingWindow.py " + str(k) + " " + str(w) + " " + str(p) + " " + str(step) + " " + file)

	# k,w,p,steps,file,algorithm
