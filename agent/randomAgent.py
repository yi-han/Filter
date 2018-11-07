"""
Middleman between the experiment and the sarsa agent. Called centralised 
due to use of a singular sarsa AI but is compatble with multiple to one states.

#TODO 

1) I think the update is wrong. Confirm that experiment is sending the right state
2) Update bug, using same state twice
# DONE
2) We should only keep track of last 3 saves, don't keep all due to memory / needless
3) Implemet checkpoint file of just the latest

"""


#import tileCoding

import agent.agentBase as aBase
import math
import numpy as np


class Agent(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, tileCoding, alph=0.1, gam=0, debug=False, test=False):

        super().__init__(pre_train_steps, debug, test)
        self.N_action = N_action
        self.N_state = N_state



    def __enter__(self):
        # probably have memory management here
        print("__enter__ random")

        return

    def __exit__(self, type, value, tb):
        # have memory management here
        print("__exit__ random")
        return

    def reset(self):
        return

    def predict(self, state, total_steps, e):        

        action = np.random.randint(0,self.N_action)
        return action 



    def update(self, last_state, last_action, current_state, is_finished, reward, next_action = 0):
        return
    def actionReplay(self, current_state, batch_size):
        return None

    def loadModel(self, load_path):
        return

    def saveModel(self, load_path, i):

        return


    def printStats(self):
        return

    def getName(self=None):
        return "RandomAgent"
    
    # def getName(self):
    #     return Agent.getName()

    def getPath(self):
        return Agent.getName()

