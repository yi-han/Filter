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

    def __init__(self, N_action, pre_train_steps, action_per_throttler, N_state, sub_agent_list,
        tau=0.1, discountFactor=0, debug=False, test=False):

        self.num_agents = len(sub_agent_list)
        self.action_per_throttler = action_per_throttler
        self.N_action = N_action # number of actions by each subAgent
        #assert action_per_throttler**self.num_agents==N_action # confirm the numbers add up
        self.agents = sub_agent_list
        self.score = 0
        self.test = test
        #self.getStatelet = getStateletFunction
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
        # print("\n\nmaking a prediction")
        #print(state)
        for i in range(len(self.agents)):
            # number of states is number of agents
            
            # print(self.agents[i])
            #print(self.agents[0].N_action)
            agent = self.agents[i]
            #N_state = agent.N_state
            #(statelet, state) = self.getStatelet(state, N_state)
            statelet = state[i]
            #print(statelet)
            agentAction = agent.predict(statelet, total_steps, e)
            # print("{0} for {1}".format(agentAction, statelet))
            #print("agent has {0} actions".format(agent.N_action))
            action = action*agent.N_action+agentAction
        # print("final action {0}".format(action))

        return action

    def update(self, last_state, network_action, current_state, is_done, reward, next_action=None):
        # provide the update function to each individual state

        #actions = AgentOfAgents.actionToActions(action, self.num_agents, self.action_per_throttler)
        N_action_list = [agent.N_action for agent in self.agents]
        actions = AgentOfAgents.genericActionToactions(network_action, N_action_list)
        # print("\nupdate")
        # print(N_action_list)
        # print("state {0}".format(last_state))
        # print("action was {0}".format(network_action))
        for i in range(len(self.agents)):
            agent = self.agents[i]
            action = actions[i]
            N_state = agent.N_state
            #(last_statelet, last_state) = self.getStatelet(last_state, N_state)
            last_statelet = last_state[i]
            # print("action was {0}".format(action))
            # print("statelet for {0} is {1}".format(i, last_statelet))
            #(current_statelet, current_state) = self.getStatelet(current_state, N_state)
            current_statelet = current_state[i]
            #print("future statelet is {0}".format(current_statelet))

            # print("for {0} we have a state of {1} and performed {2}".format(N_state, last_statelet, action))
            #print("do the actions line up?")
            agent.update(last_statelet, action, current_statelet, is_done, reward)
        self.score += reward

    def actionReplay(self, current_state, batch_size):
        # print(batch_size)
        # print(current_state)
        l = 0
        for i in range(len(self.agents)):
            agent = self.agents[i]
            N_state = agent.N_state
            # print("feed it {0} state".format(current_state[(i*N_state):((i+1)*N_state)]))
            #(current_statelet, current_state) = self.getStatelet(current_state, N_state)
            current_statelet = current_state[i]
            l+= agent.actionReplay(current_statelet, batch_size)
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
        return ("GenericDec-"+self.agents[0].getName())

    def getPath(self):
        return AgentOfAgents.getName(self)



    def reset(self):
        for agent in self.agents:
            agent.reset()

    def genericActionToactions(network_action, N_action_list):
        actions = []
        #print("")
        #print(network_action)
        #print(N_action_list)
        for N_state in N_action_list[::-1]:
            action = network_action%N_state
            #print(action)
            network_action-=action
            actions.insert(0,action)
            assert(network_action%N_state==0)
            network_action/=N_state
            network_action=int(network_action)
        #print(actions)
        #print("\n")
        return actions

#             action = action*agent.N_action+agentAction


