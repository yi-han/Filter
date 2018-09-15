from settings import *
import sys
assert(len(sys.argv)==2)

start_num = int(sys.argv[1])

for i in range(start_num):
    experiment.run(i)