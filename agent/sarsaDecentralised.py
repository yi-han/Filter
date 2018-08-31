"""
Composed of many sarasa AIs but presents a coherent system to experiment.

Deals with the translating a single state to many states and converting many actions to single action

#TODO

1) Currently making large assumption 



"""
import agent.sarsaCentralised as centralAgent
import agent.agentBase as aBase
import math


class Agent(aBase.Agent):
    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, alph=0.1, gam=0, debug=False, test=False):

        # creates an agent for each filter

        self.num_agents = int(round(math.log(N_action, action_per_agent)))
        self.action_per_agent = action_per_agent

        assert action_per_agent**self.num_agents==N_action

        self.agents = []
        for i in range(self.num_agents):
            indiv_agent = centralAgent.Agent(action_per_agent, pre_train_steps, action_per_agent, 1, alph = alph, gam=gam, debug=debug, test=test)
            self.agents.append(indiv_agent)
        self.score = 0

    def __enter__(self):
        print("__enter__ sarsaDecentralised")

    def __exit__(self, type, value, tb):
        # have memory management here
        print("__exit__ sarsaDecentralised")
        return

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

    def update(self, last_state, last_action, current_state, is_finished, reward):

        # provide the update function to each individual state
        actions = Agent.actionToActions(last_action, self.num_agents, self.action_per_agent)
        for i in range(len(last_state)):
            self.agents[i].update([last_state[i]], actions[i], current_state[i], is_finished, reward)
        self.score += reward


    def actionReplay(self, current_state, batch_size):
        return None

    def loadModel(self, load_path):
        # note we are going to use the index of the array as an id
        print("loading all models")
        for i in range(len(self.agents)):
            individual_path = load_path+'/{0}/'.format(i)
            self.agents[i].loadModel(individual_path)

    def saveModel(self,load_path, interation):
        #print("saving all models")
        for i in range(len(self.agents)):
            individual_path = load_path+'/{0}'.format(i)
            self.agents[i].saveModel(individual_path, interation)     

    def getName():
        return "SarsaDecentralisedAgent"

    def getPath():
        return "./filter"+Agent.getName()





