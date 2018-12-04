"""
Middleman between the experiment and the linear sarsa agent. Called centralised 
due to use of a singular sarsa AI but is compatble with multiple to one states.

#TODO 



"""
from agent.sarsaFunctionAI import *
import agent.agentBase as aBase
import numpy as np
import pickle
from pathlib import Path
import os
from sklearn.externals import joblib
class Agent(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, encoders, alph=0.1, gam=0, debug=False, test=False):

        super().__init__(pre_train_steps, debug, test)
        self.ai = SarsaFunctionAI(
            actions=range(N_action), encoders = encoders, alpha=alph, gamma=gam)


        self.N_action = N_action
        self.N_state = N_state
        self.score = 0
        self.test = test
        self.encoders = encoders

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
            action = self.ai.chooseAction(state)

        return action 




    def update(self, last_state, last_action, current_state, is_finished, reward, next_action = 0):
        # Note by having delta as 0, the whole point of sarsa is gone?
        # Simply a case of what has the best reward

        """
        We need the state / action / reward of one set

        Then state and action of planned next?
        """

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
            #checkpoint_file = open(checkpoint_path, 'w')
            checkpoint_file.write(name)
        
        if last_checkpoint and Path(load_path+'/'+last_checkpoint).is_file():
            # delete redundant datafile that was prior checkpoint
            # this happens at the end
            os.remove(load_path+'/'+last_checkpoint)

        with open(load_path+"/joblibBackup.sav", 'wb') as backupSave:
            # backupPickle.write("hello")
            joblib.dump(dataDict, backupSave) 

        return
    def printStats(self):
        print(self.ai.getData())


    def getName(self=None):
        return "LinearSarsaCentralisedAgent"
    
    # def getName(self):
    #     return Agent.getName()

    def getPath(self):
        return Agent.getName()

