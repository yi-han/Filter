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
adversaries = ["Constant-Attack", "Gradual-Increase", "Pulse-Large", "Pulse-Medium", "Pulse-Short"]

def condenseValues(x, y):
    # reduce to 1000 points

    y = list(y)

    block_len = len(x)/200

    nx, ny = [], []

    i = 0
    while(i*block_len<len(x)):

        nx.append(i)
        # print((i*block_len))
        # print((i+1)*block_len)
        block_y = y[int(i*block_len):(int((i+1)*block_len))]
        reduced_y = np.mean(block_y)
        ny.append(np.mean(reduced_y))
        #print(block_y)
        i+=1

    return nx, ny

def rewardGraph(directory):
    # used for the reward of the training file
    path = "{0}/reward-{1}-{2}.csv".format(directory,"train","Constant-Attack")
    print(path)
    f = pd.read_csv(path)
    

    ep_reward = f.LastReward[30000:] #f['Totalreward']
    ep = f['Episode'][30000:]

    (ep, ep_reward) = condenseValues(ep, ep_reward)

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
    num_groups = len(results.keys())

    keys = list(results.keys())

    for i in range(len(results.keys())):
        
        plt.clf()
        
        key = keys[i]
        print("\n\ndoing {0}".format(key))

        y_values = []
        names = []
        num_files = len(results[key].keys())
        for agent in results[key]:
            y_values.append(results[key][agent])
            names.append(agent)

        y_values = np.array(y_values)
        
        width = 0.2 #*(1/(num_groups*num_agents))


        ind = np.arange(num_files)
        print(ind)

        #print("yvalues - {0}".format(y_values))
        print("{0} {1}".format(y_values, names))
        plt.bar(ind, y_values, align='center', tick_label=names)
        plt.title(key)
        plt.show()

def dicToSummary(results):
    summaryFile = open("testingSummary.csv",'w')
    summaryFile.write("adversary,agent,result\n")
    for adversary in results:
        for agent in results[adversary]:
            summaryFile.write("{0},{1},{2}\n".format(adversary,agent,results[adversary][agent]))

    summaryFile.close()
    # creates a quick summary for excel

# results = getAttackStat([("decSarsa",decSarsaDir), ("decDdq", decDdqDir), ("centralDdq", cenDdqDir), ("centralSarsa", cenSarsaDir)], "ServerFailures")#"PercentageReceived")
# dicToGraph(results)
# dicToSummary(results)

rewardGraph(decSarsaDir)



