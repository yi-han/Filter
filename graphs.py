import sys
import distributions

assert(len(sys.argv)>=3)

folder = sys.argv[1]
amount = int(sys.argv[2])

if len(sys.argv)==4:
    name = sys.argv[3]
else:
    name = None

reward_types = ["reward", "init-reward", "final-reward"]
# reward_types = ["reward"]

for reward_type in reward_types:
    distributions.reward_graph(folder, reward_type, amount, name)
