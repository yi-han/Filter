import sys
import distributions

assert(len(sys.argv)>=3)

directory = sys.argv[1]
amount = int(sys.argv[2])

if len(sys.argv)==4:
    name = sys.argv[3]
else:
    name = None

reward_types = ["reward"]#, "init-reward", "final-reward"]
# reward_types = ["reward"]

for reward_type in reward_types:
    distributions.distributions(directory, amount, 190000)
    distributions.reward_graph(directory, reward_type, amount, name)
