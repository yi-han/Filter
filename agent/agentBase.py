from abc import ABCMeta, abstractmethod
from numpy import random as random

"""
This is intended as a interface for all agents
the intention is that we can swap differnt agents seemlessly
and by only these conditions nothing changes

"""

class Agent():    

    #@abstractmethod
    def __init__(self):
        return

    @abstractmethod
    def reset(self):
        pass

    # Given state, generate an action
    @abstractmethod
    def predict(self, state, total_steps, e):
        pass

    # provided the last state and the current state and prior actoin, update the learning agent
    @abstractmethod
    def update(self, last_state, last_action, current_state,d, r):
        pass


    # @abstractmethod
    def getName():
        pass

    # @abstractmethod
    def getPath():
        pass

    # @abstractmethod
    def actionReplay():
        # note not used in sarsa
        pass

    # @abstractmethod
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
        return (random.rand(1) < e)

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

            