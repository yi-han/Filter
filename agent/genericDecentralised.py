"""
I want a multiple groups of DDQN, we're going to try to make a generic 
decentralised solution


"""

"""
Comprised of many DDQN networks with one per filter

More of an interface where experiment will see only agent however
the calculations are done by many agents

"""

#import agent.agentBase as aBase
import math
import os

class AgentOfAgents():

    def __init__(self, sub_agent_list, agent_settings, network_settings):

        self.num_agents = len(sub_agent_list)
        self.action_per_throttler = network_settings.action_per_throttler
        self.agents = sub_agent_list
        self.score = 0
        self.history_size = agent_settings.history_size
        self.agent_settings = agent_settings
        self.N_state = network_settings.N_state

    
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




    def predict(self, state, e):
        # only provide each agent with its corresponding state
        # combine the actions as if it was a unified response
        # this is as network only takes a single number for action
        # combination
        action = 0
        # print("\n\npredictions")
        prediction_as_list = []
        for i in range(len(self.agents)):
            # number of states is number of agents

            agent = self.agents[i]

            statelet = state[i]
            #print(statelet)
            agentAction = agent.predict(statelet, e)
            prediction_as_list.append(agentAction)
            # print("Agent {2} | State - {0} | Action - {1}".format(statelet, agentAction, i))
        self.past_predictions.pop(0)
        self.past_predictions.append(prediction_as_list)
        return prediction_as_list

    def update(self, last_state, last_network_action, next_state, is_done, reward, next_action):
        # provide the update function to each individual state

        last_actions = last_network_action


        if last_network_action == None:
            last_network_action = [0]*self.N_state
        # print("\n Updates")
        for i in range(len(self.agents)):
            agent = self.agents[i]
            last_action = last_actions[i]
            N_state = agent.N_state
            #(last_statelet, last_state) = self.getStatelet(last_state, N_state)
            last_statelet = last_state[i]
            # print("action was {0}".format(action))
            # print("statelet for {0} is {1}".format(i, last_statelet))
            #(next_statelet, next_state) = self.getStatelet(next_state, N_state)
            next_statelet = next_state[i]
            #print("future statelet is {0}".format(next_statelet))
            # print("Agent {0} | PriorState {1} | PriorAction {2} | Reward {3}".format(i, last_statelet, last_action, reward))
            # print("for {0} we have a state of {1} and performed {2}".format(N_state, last_statelet, action))
            #print("do the last_actions line up?")
            agent.update(last_statelet, last_action, next_statelet, is_done, reward, next_action[i])
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

    def loadModel(self, load_path, prefix):
        # note we are going to use the index of the array as an id
        print("loading all models")
        for i in range(len(self.agents)):
            individual_path = load_path+'/{0}-{1}'.format(i, prefix)

            last_checkpoint = self.agents[i].loadModel(individual_path)
        return last_checkpoint # note all should have returned same value

    def saveModel(self,load_path, interation, prefix):
        for i in range(len(self.agents)):
            individual_path = load_path+'/{0}-{1}'.format(i, prefix)
            self.agents[i].saveModel(individual_path, interation)

    def getName(self):
        #print(self.agents)
        return ("GenericDec-"+self.agents[0].getName())

    def getPath(self):
        return AgentOfAgents.getName(self)



    def reset_episode(self, net):
        # for agent in self.agents:
        #     agent.reset()
        self.past_predictions = [[0]*self.num_agents]*20
        for i in range(len(self.agents)):
            self.agents[i].reset_state(net.throttlers[i], 10)

    def update_state(self, net):
        for i in range(len(self.agents)):
            self.agents[i].calculate_state(net.throttlers[i])



    def get_state(self):
        state = []
        for i in range(len(self.agents)):
            state.extend(self.agents[i].agent_state[-self.history_size:])
        return state



    def genericActionToactions(network_action, N_action_list):
        
        actions = []
        #print("")

        for N_state in N_action_list[::-1]:
            action = network_action%N_state
            network_action-=action
            actions.insert(0,action)
            if network_action%N_state!=0:
                print(network_action)
                print(N_action_list)
                print(action)
                assert(1==2)              
            network_action/=N_state
            network_action=int(network_action)
        # print(actions)
        # print("\n")
        return actions

    #             action = action*agent.N_action+agentAction
    


    def get_max_agent_value(self):
        max_agent_value = 10
        agent_tilings = 1
        return max_agent_value, max_agent_value, agent_tilings


