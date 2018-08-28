from abc import ABCMeta, abstractmethod
from numpy import random as random

"""
This is intended as a interface for all agents
the intention is that we can swap differnt agents seemlessly
and by only these conditions nothing changes

"""

class Agent():    


    def __init__(self, pre_train_steps, debug=False, test=False):
        self.pre_train_steps = pre_train_steps
        self.debug = debug
        self.test= test

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def update(self):
        pass


    @abstractmethod
    def getName():
        pass


    def isRandomGuess(self, total_steps, e):
        # calculate if meant to do choose a random
        return (random.rand(1) < e or total_steps < self.pre_train_steps) and not self.debug and not self.test
            