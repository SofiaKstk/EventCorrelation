import os

for k in range(0, 8):
	for p in range(0,1):
		for step in [1, 2, 3]:
			file = "results/stepwise/step" + str(k) + str(p) + str(step) + ".txt"
			print("stepwiseCorr.py " + str(k) + " " + str(p) + " " + str(step) + " " + file)
			os.system("stepwiseCorr.py " + str(k) + " " + str(p) + " " + str(step) + " " + file)