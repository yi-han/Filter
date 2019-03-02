"""
File generates graphs decentralised


"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

decSarsaFilter = "./filterSarsaDecentralisedAgent"
cenSarsaFilter = "./filterSarsaCentralisedAgent"

decSarsaDir = "./trainedSarsaDecentralisedAgent"
cenSarsaDir = "./trainedSarsaCentralisedAgent"

decDdqDir = "./trainedDecentralisedDDQN"
cenDdqDir = "./trainedCentralisedDDQN"

cenDdqFilter = "./filterCentralisedDDQN"
"""
mucking around directories
"""

centralised_sarsa_twensixty = "./sarsaCen2060"

sarsa_malialis = "./sarsaDecMalialis"
no_pretrain_dec_sarsa = "./noPretrainSarsaDecentralisedAgent"
twenty_same = "./filterSarsaDecTwentyDiffernt"

sarsa_short = "./sarsaDecExploration1000"


adversary_prelude = "/packet_served-test-"
adversaries = ["Constant-Attack", "Gradual-Increase", "Pulse-Large", "Pulse-Medium", "Pulse-Short"]

def condense_values(x, y):
    # reduce to 1000 points

    y = list(y)

    block_len = 4#len(x)/2000

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

def reward_single(directory,reward_prefix="reward"):
    path = "{0}/{1}-{2}-{3}.csv".format(directory, reward_prefix, "train","Constant-Attack")
    f = pd.read_csv(path)    
    ep_reward = f.LastReward#[30000:] #f['Totalreward']
    ep = f['Episode']#[30000:]

    #(ep, ep_reward) = condense_values(ep, ep_reward)
    return (ep, ep_reward)

def reward_multiple(directory, max_num, reward_prefix, PerLegitTraffic=False, Loss = False):
    # we do first one manually then loop for rest
    

    path = "{0}/{1}-{2}.csv".format(directory, reward_prefix, 0)
    print(path)
    f = pd.read_csv(path)
    if PerLegitTraffic:
        ep_reward = f.PerPacketIdeal#PerPacketIdeal #LastReward
    elif Loss:
        ep_reward = f.EpDefLoss
    else:
        ep_reward = f.LastReward

    ep = f['Episode']

    average_reward = np.zeros((len(ep),1), dtype=float)

    for i in range(max_num):
        print(i)
        path = "{0}/{1}-{2}.csv".format(directory, reward_prefix, i)
        print(path)
        f = pd.read_csv(path)
        if PerLegitTraffic:
            ep_reward = np.array(f.PerPacketIdeal, dtype=float)  #PerPacketIdeal, dtype=float)
        elif Loss:
            ep_reward = np.array(f.EpDefLoss, dtype=float)
        else:
            ep_reward = np.array(f.LastReward, dtype=float)
        ep_reward.shape=(len(ep),1)
        average_reward += ep_reward

    average_reward/=max_num
    average_reward = average_reward.tolist()
    #(ep, average_reward) = condense_values(ep, average_reward)
    return (ep, average_reward)






def reward_graph(directory, reward_type, max_num = None, title=None, PerLegitTraffic = False, Loss = False):
    # used for the reward of the training file
    
    #print(path)
   
    if not max_num:
        assert(1==2)
        (ep, ep_reward) = reward_single(directory, reward_type)
    else:
        (ep, ep_reward) = reward_multiple(directory, max_num, reward_type, PerLegitTraffic, Loss)

    if PerLegitTraffic:
        plt.ylim(0, 1)#((-0.8, 1.2))
    elif Loss:
        plt.ylim(0, 0.2)
    else:
        plt.ylim(-0.8, 1.2)
    plt.plot(ep,ep_reward, 'o-')
    if title:
        plt.title(title)
    plt.show()


 
#packet_served_file = open("{0}/packet_served-{1}-{2}.csv".format(path,run_mode,adversary.getName()),"w")

#reward_graph(decSarsaDir)

def get_attack_stat(systemsUsed,columnName):
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

def dic_to_graph(results):
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

def dic_to_summary(results):
    summaryFile = open("testingSummary.csv",'w')
    summaryFile.write("adversary,agent,result\n")
    for adversary in results:
        for agent in results[adversary]:
            summaryFile.write("{0},{1},{2}\n".format(adversary,agent,results[adversary][agent]))

    summaryFile.close()
    # creates a quick summary for excel

def distributions(directory, max_num = None, start_point=0, attack_name="", PerLegitTraffic = False, Loss=False):
    if not max_num:
        (ep, ep_reward) = reward_single(directory)
    else:
        (ep, ep_reward) = reward_multiple(directory, max_num, attack_name, PerLegitTraffic, Loss)
    print(len(ep_reward))

    ep_reward = np.array(ep_reward[start_point:])
    print("Mean = {0}".format(np.mean(ep_reward)))
    print("Median = {0}".format(np.median(ep_reward)))
    print("1Q: {0} - 2Q: {1} 2: {2}".format(np.percentile(ep_reward,25), np.percentile(ep_reward, 50),
        np.percentile(ep_reward, 75)))



# results = get_attack_stat([("decSarsa",decSarsaDir), ("decDdq", decDdqDir), ("centralDdq", cenDdqDir), ("centralSarsa", cenSarsaDir)], "ServerFailures")#"PercentageReceived")
# dic_to_graph(results)
# dic_to_summary(results)



# distributions(cenSarsaFilter, 15, 12001)
# distributions(decSarsaFilter, 15, 2000)


