"""
File generates graphs decentralised


"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

decSarsaDir = "./trainedSarsaDecentralisedAgent"
cenSarsaDir = "./trainedSarsaCentralisedAgent"

decDdqDir = "./trainedDecentralisedDDQN"
cenDdqDir = "./trainedCentralisedDDQN"


adversary_prelude = "/packet_served-test-"
adversaries = ["Constant-Attack", "Pulse-Medium"]

def rewardGraph(directory):
    # used for the reward of the training file
    path = "{0}/reward-{1}-{2}.csv".format(directory,"train","Constant-Attack")
    print(path)
    f = pd.read_csv(path)
    

    ep_reward = f.LastReward[30000:] #f['Totalreward']
    ep = f['Episode'][30000:]



    plt.plot(ep,ep_reward, 'o-')
    plt.show()


 
#packet_served_file = open("{0}/packet_served-{1}-{2}.csv".format(path,run_mode,adversary.getName()),"w")

#rewardGraph(decSarsaDir)

def getAttackStat(systemsUsed,columnName):
    names = [i[0] for i in systemsUsed]
    directories = [i[1] for i in systemsUsed]

    results = {}

    for adv in adversaries:
        results[adv] = {}
        for i in range(len(directories)):
            dire = directories[i]
            name = names[i]

            path = dire+adversary_prelude+adv+".csv"
            f = pd.read_csv(path)

            percentSucceedList = f[columnName]
            mean = np.mean(percentSucceedList)
            results[adv][name]=mean

    return results

def dicToGraph(results):
    print(results)
    ax = plt.subplot(111)
    num_groups = len(results.keys())

    for i in range(len(results.keys())):
        keys = list(results.keys())
        key = keys[i]
        y_values = []
        names = []
        num_agents = 0
        for agent in results[key]:
            y_values.append(results[key][agent])
            names.append(agent)
            num_agents += 1

        width = 0.2 *(1/(num_groups*num_agents))

        x = (width*num_agents + 0.5)*i 

        print("width - {0} | x - {1}".format(width, x))

        print("{0} {1}".format(y_values, names))
        ax.bar(x, y_values, width = (1/num_groups), align='edge', tick_label=names)


    plt.show()

# results = getAttackStat([("decSarsa",decSarsaDir)], "PercentageReceived")
# dicToGraph(results)

rewardGraph(decSarsaDir)



