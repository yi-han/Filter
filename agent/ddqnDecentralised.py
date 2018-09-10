"""
Comprised of many DDQN networks with one per filter

More of an interface where experiment will see only agent however
the calculations are done by many agents

"""

import agent.ddqnCentralised as centralAgent
import agent.agentBase as aBase
import math


class Agent(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, tau=0.1, discountFactor=0, debug=False, test=False):

        self.numAgents = int(round(math.log(N_action, action_per_agent)))
        self.action_per_agent = action_per_agent
        
        assert action_per_agent**self.numAgents==N_action

        self.agents = []
        for i in range(self.numAgents):
            # note we set the number of states as one as we have autonomous agents
            indivAgent = centralAgent.Agent(action_per_agent, pre_train_steps, action_per_agent, 1, tau, discountFactor, debug, test)
            self.agents.append(indivAgent)
        self.score = 0
        self.test = test

    def __enter__(self):
        print("__enter__ decentralised")
        for agent in self.agents:
            #agent.__enter__()
            #agent.sess = tf.Session()
            agent.sess.run(agent.init)

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

        for i in range(len(state)):
            # number of states is number of agents
            agent = self.agents[i]
            agentState = [state[i]] # in a list to mock centralised
            agentAction = agent.predict(agentState, total_steps, e)
            action = action*10+agentAction
        return action

    def update(self, last_state, action, current_state, is_done, reward, next_action=None):
        # provide the update function to each individual state
        actions = Agent.actionToActions(action, self.numAgents, self.action_per_agent)
        for i in range(len(last_state)):
            self.agents[i].update([last_state[i]], actions[i], [current_state[i]], is_done, reward)
        self.score += reward

    def actionReplay(self, current_state, batch_size):
        l = 0
        for i in range(len(current_state)):
            l+= self.agents[i].actionReplay([current_state[i]], batch_size)

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

    def getName():
        return "DecentralisedDDQN"

    def getPath(self):
        if self.test:
            prefix="./trained"
        else:
            prefix = "./filter"
        return prefix+Agent.getName()






