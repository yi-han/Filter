import sys
import os
import pandas
import matplotlib.pyplot as plt
import numpy as np
assert(len(sys.argv)==2)

sys.path.insert(0, '/Users/jeremypattison/LargeDocument/researchProject/Filter')

currentLocation = sys.argv[1]

def calcAveragePacket(location, attack_name):

    repetitionsScores = [] # note this groups by repetitions
    for prefix in range(20):
        packet_path = "{0}/packet_served-test_short-{1}-{2}.csv".format(location, attack_name, prefix)
        if os.path.exists(packet_path):
            packet_file = pandas.read_csv(packet_path)
            percentage_received = packet_file.PercentageReceived
            repetitionsScores.append(percentage_received)



    num_episodes = len(repetitionsScores[0])
    num_repetitions = len(repetitionsScores)
    print(num_episodes)
    average_reward = np.zeros((num_episodes,1), dtype=float)
    #print(average_reward)
    for i in range(num_episodes):
        for j in range(num_repetitions):
            average_reward[i] += repetitionsScores[j][i]
        average_reward[i]/=num_repetitions
    average_reward*=100 # convert percentage
    #print(average_reward)
    return np.asarray(average_reward)


constantAttack = calcAveragePacket(currentLocation, 'Constant-Attack')

attack_name = "ddAimdAltRolesSingle"
ddAttack = calcAveragePacket(currentLocation, attack_name)

diffFile = open("{0}/diffPacket-{1}.csv".format(currentLocation,attack_name), "w")

diffFile.write("Episode,Constant,IDA,IdaMinusConstant\n")
for ep_num in range(len(ddAttack)):
    diffFile.write("{0},{1},{2},{3}\n".format(ep_num, constantAttack[ep_num][0], ddAttack[ep_num][0], ddAttack[ep_num][0]-constantAttack[ep_num][0]))

diffFile.close()
