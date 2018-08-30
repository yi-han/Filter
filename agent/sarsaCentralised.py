"""
Middleman between the experiment and the sarsa agent. Called centralised 
due to use of a singular sarsa AI but is compatble with multiple to one states.

#TODO I think the update is wrong. Confirm that experiment is sending the right state



"""
from agent.sarsaAI import *
import agent.agentBase as aBase
import numpy as np



class Agent(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, alph=0.1, gam=0, debug=False, test=False):

        super().__init__(pre_train_steps, debug, test)
        self.ai = SarsaAI(
            actions=range(N_action), alpha=alph, gamma=gam)
        self.N_action = N_action
        self.lastAction = None
        self.lastState = None
        self.score = 0

    def __enter__(self):
        # probably have memory management here
        print("__enter__ sarsaCentralised")

        return

    def __exit__(self, type, value, tb):
        # have memory management here
        print("__exit__ sarsaCentralised")
        return


    def predict(self, state, total_steps, e):
        randomChoice = super().isRandomGuess(total_steps, e)
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            state = tileState(state)
            action = self.ai.chooseAction(state)

        return action 



    def update(self, last_state, last_action, current_state, is_finished, reward):
        last_state = tileState(last_state)
        
        self.score += reward

        self.last_state = last_state

        if self.lastAction is not None:
            self.ai.learn(
                self.lastState, self.lastAction, reward, last_state, last_action)
        self.lastState = last_state
        self.lastAction = last_action   

    def actionReplay(self, current_state, batch_size):
        return None

    def loadModal(self, load_path):
        #TODO: finish this
        return

    def saveModel(self, load_path, i):
        #TODO: finish this
        return

    def getName():
        return "SarsaCentralisedAgent"

    def getPath():
        return "./filter"+Agent.getName() 

def tileState(state):
    # a hack job at tileCoding. Based on 0 research or effort
    newState = []
    for el in state:
        newState.append(round(el, 1))
    return tuple(newState)


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
