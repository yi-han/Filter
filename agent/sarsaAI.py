# code initially sourced by https://github.com/studywolf/blog/tree/master/RL




import random


class SarsaAI:
    def __init__(self, actions, alpha=0.1, gamma=0): 
        # note i set gamma to 0 to reflect the implementation by Malialis
        self.q = {}

        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions


    def getQ(self, state, action):
        # used for associating with reward of new state/action. 
        # Not useful in initial implementation 
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):

        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward 
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def reset(self):
        self.q = {}


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

    def getActionChoices(self, state):
        q_list = []
        for a in self.actions:
            q_list.append((a, self.getQ(state, a)))

        return q_list


    def learn(self, state1, action1, reward, state2, action2):
        
        qnext = self.getQ(state2, action2)
        self.learnQ(state1, action1, reward, reward + self.gamma * qnext)


    def getData(self):
        #return a dict of all the information of the agent
        data = {}
        data['q']=self.q
        data['alpha'] = self.alpha
        data['gamma'] = self.gamma
        data['actions'] = self.actions

        return data

    def loadData(self, dataDict):
        # given a dictionary of preloaded values check that parameters fit
        # the current experiment and then load the q values

        if dataDict['alpha'] != self.alpha or dataDict['gamma'] != self.gamma or \
            dataDict['actions'] != self.actions:
            raise ValueError('Experiments parameters do not match saved file')
        else:
            self.q = dataDict['q']
            




