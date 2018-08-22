"""
#TODO

1) Get rid of epsilon stuff (for now), seems to be handled by bigger thing

"""
from agent.sarsaAI import *
import numpy as np



class Agent():

    def __init__(self, numActions, eps=0.3, alph=0.1, gam=0):

        self.ai = SarsaAI(
            actions=range(numActions), epsilon=eps, alpha=alph, gamma=gam)
        self.lastAction = None
        self.lastState = None
        self.score = 0

    def makeGuess(self, state):
        state = tileState(state)
        action = self.ai.chooseAction(state)
        return action 

    def update(self, state, action, reward):
        state = tileState(state)
        
        # print("doing an update")
        # print(self.lastAction)
        # print(reward)
        # print(state)
        self.score += reward

        self.state = state

        if self.lastAction is not None:
            self.ai.learn(
                self.lastState, self.lastAction, reward, state, action)
        self.lastState = state
        self.lastAction = action   

    def reset(self):
        # i think it should just put into a random state
        # alternatively i think there is preset states from net. See that
        
        self.lastAction = None
        self.lastState = None
        #         here = self.cell
        # if here.goal or here.cliff:
        #     self.cell = startCell
        #     self.lastAction = None
        # else:
        #     self.goInDirection(action)


def tileState(state):
    # a hack job at tileCoding. Based on 0 research or effort
    #print(state)
    return round(state[0], 1)  


"""
mock stuff to see if i can get it to work

def calcReward(state):
    if state == 3:
        #return round(np.random.random_sample(size=None)*2-1,3)
        return 1
    else:
        return -1

def nextState(action):
    if action == 2 and (np.random.rand() <0.8):
        return 3

    return np.random.randint(3, size=None)


agent = Agent(3)

reward = 0.2
action = 2
count = 0
while(True):
    count += 1
    state = nextState(action)
    reward = calcReward(state)
    action = agent.makeGuess(state)

    agent.update(state, action, reward)
    

    #print("state = {0} - action = {1} - reward = {2}".format(state,action,reward))
    if count%100 == 0:
        print("count = {0}, sumReward = {1}".format(count, agent.score))
    if count > 1000:
        print(action)

"""
