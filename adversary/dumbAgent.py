"""
The dumb agent allows the user to test traditonal attack strategies against the defender

As it follows an attacking strategy, the individual agents do not make a choice.

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




    def addLeaves(self, leaves):
        for leaf in leaves:
            assert(not leaf in self.leaves)
            self.leaves.append(leaf)

    def sendTraffic(self, action):
        # we distribute all the legitimate traffic + adversarial traffic
        # legitimate traffic is constant, adversarial traffic is dependent ono action


        # send legitimate traffic
        # legal_per_leaf = self.legal_traffic/len(self.leaves)

        percent_emit = action/10
        
        # illegal_per_leaf = self.illegal_traffic * percent_emit / len(self.leaves)
        for leaf in self.leaves:
            leaf.sendTraffic(percent_emit)
            # leaf.destination_switch.new_legal += legal_per_leaf
            # leaf.destination_switch.new_illegal += illegal_per_leaf


    def initiate_episode(self):
        
        # If we're random this is when we choose a random attack method
        # If we're loading this is when we load the attack method (save as an enum)
        return



