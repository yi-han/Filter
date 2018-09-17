import sys
import distributions

assert(len(sys.argv)>=3)

folder = sys.argv[1]
amount = int(sys.argv[2])

if len(sys.argv)==4:
    name = sys.argv[3]
else:
    name = None


distributions.reward_graph(folder,amount, name)
