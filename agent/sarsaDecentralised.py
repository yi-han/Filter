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

    def __init__(self, numActions, pre_train_steps, actionPerAgent = 10, alph=0.1, gam=0, debug=False, test=False):

        # creates an agent for each filter

        self.numAgents = int(round(math.log(numActions, actionPerAgent)))
        self.actionPerAgent = actionPerAgent

        assert actionPerAgent**self.numAgents==numActions

        self.agents = []
        for i in range(self.numAgents):
            indivAgent = centralAgent.Agent(actionPerAgent, pre_train_steps, alph = alph, gam=gam, debug=debug, test=test)
            self.agents.append(indivAgent)
        self.score = 0

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

    def update(self, state, action, reward):
        # provide the update function to each individual state
        actions = actionToActions(action, self.numAgents, self.actionPerAgent)
        for i in range(len(state)):
            self.agents[i].update([state[i]], actions[i], reward)

        self.score += reward


    def reset(self):
        # reset each agent
        for i in range(len(self.agents)):
            self.agents[i].reset()

    def getName():
        return "SarsaDecentralisedAgent"

    def actionReplay(self, currentState):
        return None

def actionToActions(action, numAgents, actionPerAgent):
    # takes the action presented to network and returns
    # a list of each action by each agent
    actions = []
    numAgents-=1
    while(numAgents>=0):

        divider = actionPerAgent**numAgents
        individualAction = int(action/divider)
        action -= (individualAction*divider)
        numAgents -= 1
        actions.append(individualAction)
    return actions




