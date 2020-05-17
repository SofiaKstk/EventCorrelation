import os

for algorithm in ["shewhart", "cusum"]:
	for k in range(0, 8):
		for p in range(0,1):
			for step in [1, 2, 3]:
				file = "results/stepwise/" + algorithm + "/step" + str(k) + str(p) + str(step) + ".txt"
				print("stepwise.py " + str(k) + " " + str(p) + " " + str(step) + " " + file + " " + algorithm)
				os.system("stepwise.py " + str(k) + " " + str(p) + " " + str(step) + " " + file + " " + algorithm)