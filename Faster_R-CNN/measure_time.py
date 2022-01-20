import os
from timeit import default_timer as timer


time = 0
runs = 10

for i in range(runs):
    start = timer()
    os.system('python3 frcnn_detect.py --conf-thres 0.15')
    time += timer() - start

print(time/runs)
