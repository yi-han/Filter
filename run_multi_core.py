"""
Technically this runs a single core, but its designed in a way
that a multicore system could call it repetitively to split the load

"""


import sys
from settings import *
assert(len(sys.argv)==3)

start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

for i in range(length_core):
    print("Im doing it for {0}".format(start_num+i))
    experiment.run(start_num+i)
