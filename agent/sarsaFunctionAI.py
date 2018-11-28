"""
Quick attempt using function approximation


Note using the state as the values is unlikely to 'work' probably need
to do some sort of transformation.

"""

# code initially sourced by https://github.com/studywolf/blog/tree/master/RL
# https://github.com/dennybritz/reinforcement-learning/blob/master/FA/Q-Learning%20with%20Value%20Function%20Approximation%20Solution.ipynb



import random
import numpy as np
import agent.tileCoding
#env = gym.envs.make("MountainCar-v0")



class TileWrapper(object):
    # A cheap method of introducing the bias term whilst we still work out if necessary
    def __init__(self, encoders, bias_term = False):
        self.encoders = encoders
        self.bias_term = bias_term

    def featureSize(self):
        count = 0
        for encoder in self.encoders:
            count += encoder.featureSize()
        if self.bias_term:
            count += 1
            print("\n\nadding bias")
        return count


    def feature_converter(self, state):
        state_vector = []
        # print(state)
        for i in range(len(state)):
            encoder = self.encoders[i]
            state_vector.extend(encoder.encodeToVector(state[i]))
        if self.bias_term:
                state_vector.append(1)
        # print(state)
        # print(state_vector)
        #print(np.array(state_vector))
        # print(len(state_vector))
        return np.array(state_vector)

class SarsaFunctionAI:
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
    
    def __init__(self, actions, encoders, alpha, gamma): 
        # note i set gamma to 0 to reflect the implementation by Malialis
        # alpha is learning rate
        # gamma is discount

        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.w_matrix = []
        
        self.tile_wrapper = TileWrapper(encoders)
        self.n_features = self.tile_wrapper.featureSize()
        
        self.reset()





    def getQ(self, state, action, error_check = False):
        # convert action into a vector
        action_num = self.actions.index(action)
        # print(self.w_matrix)
        w = self.w_matrix[action_num]
        state_vector = self.tile_wrapper.feature_converter(state)
        if False:
            print("\n\nstate")
            print(state)
            #print(state_vector)
            print(action)
            #print("weight")
            #print(w)
            #print(w*state_vector)
            print(np.dot(w, state_vector))

        return np.dot(w, state_vector)


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
        state_vector = self.tile_wrapper.feature_converter(state)
        self.w_matrix[action_num] = current_weights + coefficient*state_vector
        
        if False :#current_weights[-38] != 0:
            print("\naction")
            print(action)
            print(state)
            print(state_vector)
            # print("gradient")
            # print(self.tile_wrapper.feature_converter(state))
            # print("original")
            print(current_weights)
            print("coefficient")
            # print(coefficient)
            # print("difference")
            # print(coefficient/self.alpha)
            # print("new")
            # print(self.w_matrix[action_num])


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
            dataDict['actions'] != self.actions or dataDict['n_features'] != self.n_features:
            print(dataDict)
            
            raise ValueError('Experiments parameters do not match saved file')
        else:
            self.w_matrix = dataDict['w_matrix']
            



