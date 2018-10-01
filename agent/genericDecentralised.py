"""
I want a multiple groups of DDQN, we're going to try to make a generic 
decentralised solution


"""

"""
Comprised of many DDQN networks with one per filter

More of an interface where experiment will see only agent however
the calculations are done by many agents

"""

import agent.agentBase as aBase
import math


class AgentOfAgents(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_throttler, N_state, sub_agent_list, tau=0.1, discountFactor=0, debug=False, test=False):

        self.num_agents = len(sub_agent_list)
        self.action_per_throttler = action_per_throttler
        self.N_action = N_action # number of actions by each subAgent
        #assert action_per_throttler**self.num_agents==N_action # confirm the numbers add up
        self.agents = sub_agent_list
        self.score = 0
        self.test = test

    def __enter__(self):
        print("__enter__ generic decentralised")
        for agent in self.agents:
            #agent.__enter__()
            #agent.sess = tf.Session()
            #agent.sess.run(agent.init)
            agent.__enter__()

    def __exit__(self, type, value, tb):
        print("\n\ndecentralised__exit__ called\n\n")
        for agent in self.agents:
            agent.__exit__(type, value, tb)

    def predict(self, state, total_steps, e):
        # only provide each agent with its corresponding state
        # combine the actions as if it was a unified response
        # this is as network only takes a single number for action
        # combination
        action = 0

        for i in range(len(self.agents)):  #range(len(state)):
            # number of states is number of agents
            
            # print(self.agents[i])
            # print(self.agents[0].N_action)
            agent = self.agents[i]
            N_state = agent.N_state
            agentState = state[(i*N_state):((i+1)*N_state)] # in a list to mock centralised


            agentAction = agent.predict(agentState, total_steps, e)
            action = action*self.N_action+agentAction
        return action

    def update(self, last_state, action, current_state, is_done, reward, next_action=None):
        # provide the update function to each individual state
        actions = AgentOfAgents.actionToActions(action, self.num_agents, self.action_per_throttler)
        for i in range(len(last_state)):
            self.agents[i].update([last_state[i]], actions[i], [current_state[i]], is_done, reward)
        self.score += reward

    def actionReplay(self, current_state, batch_size):
        l = 0
        for i in range(len(current_state)):
            l+= self.agents[i].actionReplay([current_state[i]], batch_size)
        return l

    def loadModel(self, load_path):
        # note we are going to use the index of the array as an id
        print("loading all models")
        for i in range(len(self.agents)):
            individual_path = load_path+'/{0}'.format(i)
            self.agents[i].loadModel(individual_path)

    def saveModel(self,load_path, interation):
        for i in range(len(self.agents)):
            individual_path = load_path+'/{0}'.format(i)
            self.agents[i].saveModel(individual_path, interation)

    def getName(self):
        #print(self.agents)
        return ("Dec-"+self.agents[0].getName())

    def getPath(self):
        return AgentOfAgents.getName(self)

    def reset(self):
        for agent in self.agents:
            agent.reset()





