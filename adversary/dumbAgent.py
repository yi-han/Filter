"""
We're attempting to replace hosts with a dumb agent

"""

"""
This is a generic attacker agent that can be responsible for attacking all/one defenders.

We will then use a generic controller / master. Then allow individual masters be built on top.

"""

from agent.ddqn import *

import numpy as np
import os
import sys
from numpy import random as random
import re





class dumbAgent():
    def __init__(self):

        self.leaves = []

    
    def __enter__(self):
        print("sess init dumbAGent")



    def __exit__(self, type, value, tb):
        print("\n\ndumb __exit__ called\n\n")



        
    # def predict(self, state, e, step):
    #     if not self.leaves[0].isAttackActive(step):
    #         # if the attack is off return 0
    #         return 0        

    #     action = self.adv_settings.prediction_method(step)
    #     return action

    # def update(self, last_state, last_action, current_state, d, r, step, next_action=None):
    #     return

    # def actionReplay(self, current_state, batch_size):
    #     return 0


    # def loadModel(self, load_path):


    #     return None


    # def saveModel(self, load_path, iteration):

    #     return None


    # def getName(self=None):
    #     return "ddAdvAgent"

    # def getPath(self):
    #     return self.getName()


    def addLeaves(self, leaves):
        for leaf in leaves:
            assert(not leaf in self.leaves)
            self.leaves.append(leaf)

    def sendTraffic(self, action, time_step):
        # we distribute all the legitimate traffic + adversarial traffic
        # legitimate traffic is constant, adversarial traffic is dependent ono action


        # send legitimate traffic
        # legal_per_leaf = self.legal_traffic/len(self.leaves)

        percent_emit = action/10
        
        # illegal_per_leaf = self.illegal_traffic * percent_emit / len(self.leaves)
        for leaf in self.leaves:
            leaf.sendTraffic(percent_emit, time_step)
            # leaf.destination_switch.new_legal += legal_per_leaf
            # leaf.destination_switch.new_illegal += illegal_per_leaf


    def initiate_episode(self):
        
        # If we're random this is when we choose a random attack method
        # If we're loading this is when we load the attack method (save as an enum)
        return



