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
# from sklearn.externals import joblib
class Agent(aBase.Agent):

    def __init__(self, N_action, N_state, encoders, agent_settings):
        self.tau = agent_settings.tau
        self.discount_factor = agent_settings.discount_factor
        super().__init__()
        self.ai = SarsaFunctionAI(
            actions=range(N_action), encoders = encoders, agent_settings=agent_settings)



        self.N_action = N_action
        self.N_state = N_state
        self.score = 0
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
        # do nothing. This is intentinoal as we were resetting everythign each episode.
        assert(1==2)
        return

    def predict(self, state, e):
        randomChoice = super().isRandomGuess(e)
        

        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            action = self.ai.chooseAction(state)

        return action 




    def update(self, last_state, last_action, current_state, is_finished, reward, next_action):
        # Note by having delta as 0, the whole point of sarsa is gone?
        # Simply a case of what has the best reward

        """
        We need the state / action / reward of one set

        Then state and action of planned next?
        """
        self.score += reward


        self.ai.learn(last_state, last_action, reward, current_state, next_action)


    def actionReplay(self, current_state, batch_size):
        loss = self.ai.cumLoss
        self.ai.cumLoss = 0
        return loss

    def loadModel(self, load_path):
        # let above work out the load_path especially with the decentralised part
        print("Loading {0}".format(load_path))
        with open(load_path+"/checkpoint", 'r') as checkpoint_file:
            last_checkpoint = checkpoint_file.readline()

        print(last_checkpoint)
        picklePath = load_path+"/"+last_checkpoint
        pp = Path(picklePath)
        if pp.is_file():
            with open(picklePath, 'rb') as f:
                print("used pickle \n")
                dataDict = pickle.load(f)
        else:
            assert(5==1)
        # else:
        #     print("using joblib \n")
        #     dataDict = joblib.load(load_path+"/joblibBackup.sav") 
        
        self.ai.loadData(dataDict)


        return int(last_checkpoint[:-4])

    def saveModel(self, load_path, i):
        if not os.path.exists(load_path):
            os.makedirs(load_path) 

        checkpoint_path = load_path+'/checkpoint'
        cpp = Path(checkpoint_path)
        if cpp.is_file():
            checkpoint_file = open(checkpoint_path,'r')
            last_checkpoint = checkpoint_file.readline()
            last_checkpoint = load_path+'/'+last_checkpoint
        else:
            last_checkpoint = None

        dataDict = self.ai.getData()
        name = str(i)+'.pkl'

        current_checkpoint_path = load_path+'/'+name
        f = open(current_checkpoint_path, 'wb')
        pickle.dump(dataDict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        with open(checkpoint_path, 'w') as checkpoint_file:
            # update checkpoint to point to new datafile
            #checkpoint_file = open(checkpoint_path, 'w')
            checkpoint_file.write(name)
        
        if last_checkpoint and last_checkpoint != current_checkpoint_path and Path(last_checkpoint).is_file() and Path(current_checkpoint_path).is_file():
            # delete redundant datafile that was prior checkpoint
            # this happens at the end
            os.remove(last_checkpoint)

        # with open(load_path+"/joblibBackup.sav", 'wb') as backupSave:
            # backupPickle.write("hello")
            # joblib.dump(dataDict, backupSave) 

        return
    def printStats(self):
        print(self.ai.getData())


    def getName(self=None):
        return "LinearSarsaCentralisedAgent"
    
    # def getName(self):
    #     return Agent.getName()

    def getPath(self):
        return Agent.getName()

