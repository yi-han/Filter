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
from agent.sarsaAI import *
import agent.agentBase as aBase
import numpy as np
import pickle
from pathlib import Path
import os
class Agent(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, alph=0.1, gam=0, debug=False, test=False):

        super().__init__(pre_train_steps, debug, test)
        self.ai = SarsaAI(
            actions=range(N_action), alpha=alph, gamma=gam)
        self.N_action = N_action
        self.N_state = N_state
        print("I have {0} actions".format(self.N_action))
        self.score = 0
        self.test = test

    def __enter__(self):
        # probably have memory management here
        print("__enter__ sarsaCentralised")

        return

    def __exit__(self, type, value, tb):
        # have memory management here
        print("__exit__ sarsaCentralised")
        return

    def reset(self):
        self.ai.reset()

    def predict(self, state, total_steps, e):
        randomChoice = super().isRandomGuess(total_steps, e)
        

        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            state = tileState(state)
            action = self.ai.chooseAction(state)

        return action 

    def get_action_choices(self, state):
        state = tileState(state)
        return self.ai.getActionChoices(state)


    def update(self, last_state, last_action, current_state, is_finished, reward, next_action = 0):
        # Note by having delta as 0, the whole point of sarsa is gone?
        # Simply a case of what has the best reward

        """
        We need the state / action / reward of one set

        Then state and action of planned next?
        """

        last_state = tileState(last_state)
        current_state = tileState(current_state)
        self.score += reward


        self.ai.learn(last_state, last_action, reward, current_state, next_action)


    def actionReplay(self, current_state, batch_size):
        return None

    def loadModel(self, load_path):
        # let above work out the load_path especially with the decentralised part
        with open(load_path+"/checkpoint", 'r') as checkpoint_file:
            last_checkpoint = checkpoint_file.readline()

        with open(load_path+"/"+last_checkpoint, 'rb') as f:
            dataDict = pickle.load(f)
            print("datadic is loaded \n")
            self.ai.loadData(dataDict)


        return

    def saveModel(self, load_path, i):
        if not os.path.exists(load_path):
            os.makedirs(load_path) 

        checkpoint_path = load_path+'/checkpoint'
        cpp = Path(checkpoint_path)
        if cpp.is_file():
            checkpoint_file = open(checkpoint_path,'r')
            last_checkpoint = checkpoint_file.readline()
        else:
            last_checkpoint = None

        dataDict = self.ai.getData()
        name = Agent.getName()+'-'+str(i)+'.pkl'

        with open(load_path+'/'+name, 'wb') as f:
            # dump datafile
            pickle.dump(dataDict, f, pickle.HIGHEST_PROTOCOL)

        with open(checkpoint_path, 'w') as checkpoint_file:
            # update checkpoint to point to new datafile
            checkpoint_file = open(checkpoint_path, 'w')
            checkpoint_file.write(name)
        
        if last_checkpoint and Path(load_path+'/'+last_checkpoint).is_file():
            # delete redundant datafile that was prior checkpoint
            # this happens at the end
            os.remove(load_path+'/'+last_checkpoint)
        return
    def printStats(self):
        print(self.ai.getData())


    def getName(self=None):
        return "SarsaCentralisedAgent"
    
    # def getName(self):
    #     return Agent.getName()

    def getPath(self):
        return Agent.getName()

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
