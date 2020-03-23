import sys
import os
import pandas
import matplotlib.pyplot as plt
import numpy as np
assert(len(sys.argv)==2)

sys.path.insert(0, '/Users/jeremypattison/LargeDocument/researchProject/Filter')

currentLocation = sys.argv[1]

repetitionsScores = [] # note this groups by repetitions
for prefix in range(20):
    packet_path = "{0}/packet_served-load-ddAimdSingle-{1}.csv".format(currentLocation, prefix)
    
    if os.path.exists(packet_path):
        packet_file = pandas.read_csv(packet_path)
        percentage_received = packet_file.PercentageReceived
        repetitionsScores.append(percentage_received)


#print(repetitionsScores)
num_episodes = len(repetitionsScores[0])
num_repetitions = len(repetitionsScores)
print(num_episodes)
average_reward = np.zeros((num_episodes,1), dtype=float)
for i in range(num_episodes):
    for j in range(num_repetitions):
        average_reward[i] += repetitionsScores[j][i]
    average_reward[i]*=(100/num_repetitions)

print("ready")
plt.ylim(40, 100)
plt.xlim(0,num_episodes)
plt.scatter(list(range(num_episodes)),average_reward, s=0.1)
plt.ylabel("Legitimate traffic serviced (%)")
plt.xlabel("Episode")
frequency = num_episodes/5
plt.xticks(range(num_episodes+1)[::frequency], range(num_episodes+1)[::frequency])


plt.rcParams.update({'font.size': 22})

plt.show()