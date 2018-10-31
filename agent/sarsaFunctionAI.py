"""
Quick attempt using function approximation


Note using the state as the values is unlikely to 'work' probably need
to do some sort of transformation.

"""

# code initially sourced by https://github.com/studywolf/blog/tree/master/RL
# https://github.com/dennybritz/reinforcement-learning/blob/master/FA/Q-Learning%20with%20Value%20Function%20Approximation%20Solution.ipynb



import random
import numpy as np

#env = gym.envs.make("MountainCar-v0")



class Estimator():
    """
    Value Function approximator.
    #DONE
    1) Creates a weight vector length N
    2) Add for each action
    4) Function that takes encoder for each state
    5) Function that takes state and action and performs the necessary transformation
    6) Update rule
    7) Prediction Rule 

    #TODO 

    8) Should I be putting the encoding in the upper level?
    3) Add the normaliser at the end. CONFIRM?

    """



class SarsaFunctionAI:
    
    def __init__(self, actions, encoders, alpha, gamma): 
        # note i set gamma to 0 to reflect the implementation by Malialis
        # alpha is learning rate
        # gamma is discount

        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.w_matrix = []
        
        n_features = 0
        self.encoders=[]
        for encoder in encoders:
            n_features+=encoder.featureSize()
            self.encoders.append(encoder)

        self.n_features = n_features
        
        self.reset()



    def feature_converter(self, state):
        state_vector = []
        for i in range(len(state)):
            encoder = self.encoders[i]
            state_vector.extend(encoder.encodeToVector(state[i]))
        return np.array(state_vector)

    def getQ(self, state, action, error_check = False):
        # convert action into a vector
        action_num = self.actions.index(action)
        # print(self.w_matrix)
        w = self.w_matrix[action_num]
        state_vector = self.feature_converter(state)
        if error_check:
            print("\nstate")
            print(state)
            print(state_vector)
            print("weight")
            print(w)
            print(w*state_vector)

        return np.sum(w * state_vector)


    def reset(self):
        for action in self.actions:
            w = np.zeros(self.n_features)
            self.w_matrix.append(w)



    def chooseAction(self, state):
        # as epsilon dealt with by main we going to ignore epsilon logic for now

        # if random.random() < self.epsilon:
        #     action = random.choice(self.actions)
        # else:
        q = [self.getQ(state, a) for a in self.actions]
        maxQ = max(q)
        count = q.count(maxQ)
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)

        action = self.actions[i]
        return action


    def learnCore(self, state, action, reward):
        # assume the reward has the discount incorporated. Allows this to be used 
        # between qlearning and sarsa
        action_num = self.actions.index(action)        
        current_weights = self.w_matrix[action_num]
        coefficient = (self.alpha*(reward - self.getQ(state, action)))
        state_vector = self.feature_converter(state)
        self.w_matrix[action_num] = current_weights + coefficient*self.feature_converter(state)


    def learn(self, state1, action1, reward, state2, action2):
        # we do the sarsa step and then feed it to a generalised td learner
        qnext = self.getQ(state2, action2)
        self.learnCore(state1, action1, reward + self.gamma * qnext)


    def getData(self):
        #return a dict of all the information of the agent
        data = {}
        
        data['w_matrix']=self.w_matrix
        data['alpha'] = self.alpha
        data['gamma'] = self.gamma
        data['actions'] = self.actions
        data['n_features'] = self.n_features

        return data

    def loadData(self, dataDict):
        # given a dictionary of preloaded values check that parameters fit
        # the current experiment and then load the q values

        if dataDict['alpha'] != self.alpha or dataDict['gamma'] != self.gamma or \
            dataDict['actions'] != self.actions or data['n_features'] != self.n_features:
            raise ValueError('Experiments parameters do not match saved file')
        else:
            self.w_matrix = dataDict['w_matrix']
            


