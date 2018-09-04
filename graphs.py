"""
File generates graphs decentralised


"""
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

directory = "./trainedSarsaDecentralisedAgent"


def rewardGraph(directory):
    # used for the reward of the training file
    path = "{0}/reward-{1}-{2}.csv".format(directory,"train","Constant-Attack")
    print(path)
    f = pd.read_csv(path)
    print(f.keys())

    ep_reward = f.Lastreward #f['Totalreward']
    ep = f['Episode']


    plt.plot(ep,ep_reward, 'o-')
    plt.show()


rewardGraph(directory)