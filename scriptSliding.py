import numpy as np
from os import path
import threading
from slidingWindow import sliding
import time

def thread_function(k,w,p,step,ageing,file, algorithm):
	if str(path.exists(file)) != "True":
		sliding(k,w,p,step,ageing,file,algorithm)
		# k,w,p,steps,file,algorithm


if __name__ == "__main__":
	for k in range(1, 8):
		for w in range(3, 8):
			for step in [1, 2, 3]:
				for algorithm in ["cusum", "shewhart"]:
					for ageing in ["linear", "exponential"]:
						threads = list()
						for p in np.arange(0.4, 1.0, 0.1):
							file = "results/sliding/" + algorithm + "/" + ageing + "/sliding" + str(k) + str(w) + str(step) + "p" + str(p) + ".txt"
							print("slidingWindow.py " + str(k) + " " + str(w) + " " + str(step) + " "+ ageing + " " + file + " " +algorithm)
							
							x = threading.Thread(target=thread_function, args=(k,w,p,step,ageing,file,algorithm))
							threads.append(x)
							x.start()
							time.sleep(1)
						for thread in threads:
							thread.join()			
