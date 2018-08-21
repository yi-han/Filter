"""
What my objective is: 
1) We're just going to make a class that we feed fake data to
2) Then try to link with the main stuff

"""
import sarsaAI
import numpy as np



class Agent():

    def __init__(self, numActions):

        self.ai = sarsaAI.Sarsa(
            actions=range(numActions), epsilon=0.3, alpha=0.1, gamma=0.4)
        self.lastAction = None
        self.lastState = None
        self.score = 0

    def makeGuess(self, state):
        action = self.ai.chooseAction(state)
        return action 

    def update(self, state, action, reward):

        self.score += reward

        self.state = tileState(state)

        if self.lastAction is not None:
            self.ai.learn(
                self.lastState, self.lastAction, reward, state, action)
        self.lastState = state
        self.lastAction = action   

def tileState(state):
    # a hack job at tileCoding. Based on 0 research or effort
    return round(state, 1)  

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
    #print("\n\n")


