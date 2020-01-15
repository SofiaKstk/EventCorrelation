import os
import numpy as np
import os.path
from os import path


# for k in range(4, 8):
k=4
for w in range(6, 8):
	for p in np.arange(0.4, 1.0, 0.1):
		for step in [1, 2, 3]:
			for algorithm in ["cusum", "shewhart"]:
				file = "results/sliding/" + algorithm + "/step" + str(k) + str(w) + str(step) + "p" + str(p) + ".txt"
				print("slidingWindow.py " + str(k) + " " + str(w) + " " + str(step) + " " +algorithm + " " + file)
				if str(path.exists(file)) == "True":
					continue
				os.system("slidingWindow.py " + str(k) + " " + str(w) + " " + str(p) + " " + str(step) + " " + file + " " + algorithm)

	# k,w,p,steps,file,algorithm
