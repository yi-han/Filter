from abc import ABCMeta, abstractmethod
from numpy import random as random

"""
This is intended as a interface for all agents
the intention is that we can swap differnt agents seemlessly
and by only these conditions nothing changes

"""

class Agent():    

    #@abstractmethod
    def __init__(self, pre_train_steps, debug=False, test=False):
        self.pre_train_steps = pre_train_steps
        self.debug = debug
        self.test= test

    # @abstractmethod
    # def reset(self):
    #     pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def update(self):
        pass


    @abstractmethod
    def getName():
        pass

    @abstractmethod
    def getPath():
        pass

    @abstractmethod
    def actionReplay():
        # note not used in sarsa
        pass

    @abstractmethod
    def load_model(self,load_path):
        pass

        
    # @abstractmethod
    # def __enter__(self):
    #     pass

    # @abstractmethod
    # def __exit__(self, exception_type, exception_value, traceback):
    #     pass

    def isRandomGuess(self, total_steps, e):
        # calculate if meant to do choose a random
        return (random.rand(1) < e or total_steps < self.pre_train_steps) and not self.debug and not self.test

    def actionToActions(action, num_agents, action_per_agent):
    # takes the action presented to network and returns
    # a list of each action by each agent
        actions = []
        num_agents-=1
        while(num_agents>=0):

            divider = action_per_agent**num_agents
            individualAction = int(action/divider)
            action -= (individualAction*divider)
            num_agents -= 1
            actions.append(individualAction)
        return actions

            