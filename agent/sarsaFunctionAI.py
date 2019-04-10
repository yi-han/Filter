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

    #def feature_learn()

class qTable():
    # qtable split for every encoder. This is independent of actions
    # so the parent function would need to make one of these for each action
    def __init__(self, tile_wrapper, bias_term = False):
        # make a qtable for every encoder.
        self.w_matrix = []
        self.tile_wrapper = tile_wrapper

        for encoder in tile_wrapper.encoders:
            w = np.zeros(encoder.featureSize())
            self.w_matrix.append(w)

    def getQValue(self, state, state_vectors = False):
        # given an action what is the value?
        q_value = 0
        for i in range(len(state)):
            w = self.w_matrix[i]
            if state_vectors:
                state_vector = state_vectors[i]
            else:
                state_vector = self.tile_wrapper.encoders[i].encodeToVector(state[i])
            q_value += np.dot(w, state_vector)

            #print(state[i].size)
        return q_value

    def updateQvalue(self, state, tau, rewardPq):
        # we've calculated the policy result and now we update the matrix

        # calculate the state vectors so only use once.

        state_vectors = []
        for i in range(len(self.tile_wrapper.encoders)):
            state_vectors.append(self.tile_wrapper.encoders[i].encodeToVector(state[i]))


        delta = tau*(rewardPq - self.getQValue(state, state_vectors))


        for i in range(len(self.w_matrix)):
            current_weights = self.w_matrix[i]
            num_tilings = self.tile_wrapper.encoders[i].numTilings
            self.w_matrix[i] = (current_weights + (state_vectors[i]*(delta/num_tilings)))
        return delta
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
    
    def __init__(self, actions, encoders, agent_settings): 
        # note i set discount_factor to 0 to reflect the implementation by Malialis
        # tau is learning rate
        # discount_factor is discount

        self.actions = actions
        self.tau = agent_settings.tau
        self.discount_factor = agent_settings.discount_factor

        
        self.tile_wrapper = TileWrapper(encoders)
        self.n_features = self.tile_wrapper.featureSize()
        
        self.agent_settings = agent_settings
        self.cumLoss = 0

        self.q_tables = []
        for action in self.actions:
            self.q_tables.append(qTable(self.tile_wrapper))





    def getQ(self, state, action, error_check = False):
        # convert action into a vector
        action_num = self.actions.index(action)
        
        return self.q_tables[action_num].getQValue(state)



    def reset(self):
        assert(1==2)


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


    def learnCore(self, state, action, rewardPq):
        # assume the reward has the discount incorporated. Allows this to be used 
        # between qlearning and sarsa

        # rewardPq = discount_factor*Q(next) + reward
        action_num = self.actions.index(action)
        delta = self.q_tables[action_num].updateQvalue(state, self.tau, rewardPq)
        self.cumLoss += abs(delta)



    def learn(self, state1, action1, reward, state2, action2):
        # we do the sarsa step and then feed it to a generalised td learner
        if self.discount_factor != 0:
            qnext = self.getQ(state2, action2)
        else:
            qnext = 0
        self.learnCore(state1, action1, reward + self.discount_factor * qnext)


    def getData(self):
        #return a dict of all the information of the agent
        data = {}
        
        data['q_tables']=self.q_tables
        data['tau'] = self.tau
        data['discount_factor'] = self.discount_factor
        data['actions'] = self.actions
        data['n_features'] = self.n_features
       
        data['name'] = self.agent_settings.name

        data['num_episodes'] = self.agent_settings.num_episodes
        data['pre_train_episodes'] = self.agent_settings.pre_train_episodes
        data['annealing_episodes'] = self.agent_settings.annealing_episodes
        data['startE'] = self.agent_settings.startE
        data['reward_overload'] = self.agent_settings.reward_overload
        return data

    def loadData(self, dataDict):
        # given a dictionary of preloaded values check that parameters fit
        # the current experiment and then load the q values

        if dataDict['tau'] != self.tau or dataDict['discount_factor'] != self.discount_factor or \
            dataDict['actions'] != self.actions or dataDict['n_features'] != self.n_features:
            print("tau {0} | {1}".format(dataDict['tau'], self.tau))
            print("discount_factor {0} | {1}".format(dataDict['discount_factor'], self.discount_factor))
            print("actions {0} | {1}".format(dataDict['actions'], self.actions))
            print("n_features {0} | {1}".format(dataDict['n_features'], self.n_features))
            raise ValueError('Experiments parameters do not match saved file')
        if dataDict['name'] != self.agent_settings.name \
        or dataDict['num_episodes'] != self.agent_settings.num_episodes \
        or dataDict['startE'] != self.agent_settings.startE \
        or dataDict['reward_overload'] != self.agent_settings.reward_overload \
        or dataDict['pre_train_episodes'] != self.agent_settings.pre_train_episodes \
        or dataDict['annealing_episodes'] != self.agent_settings.annealing_episodes:
            print("name {0} | {1}".format(dataDict['name'], self.agent_settings.name))
            print("num_episodes {0} | {1}".format(dataDict['num_episodes'], self.agent_settings.num_episodes))
            print("startE {0} | {1}".format(dataDict['startE'], self.agent_settings.startE))
            print("reward_overload {0} | {1}".format(dataDict['reward_overload'], self.agent_settings.reward_overload))
            print("pre_train_episodes {0} | {1}".format(dataDict["pre_train_episodes"], self.agent_settings.pre_train_episodes))
            print("annealing_episodes {0} | {1}".format(dataDict["annealing_episodes"], self.agent_settings.annealing_episodes))

            raise ValueError("Class settings do not match")
        else:
            self.q_tables = dataDict['q_tables']
        # or dataDict['y'] != self.agent_settings.y or dataDict['tau'] != self.agent_settings.tau \
