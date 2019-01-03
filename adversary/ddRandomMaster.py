"""
Generic interface for many agents for adversary.
We assign the potentials for each agent randomally each episode
as opposed to using another agent to coordinate the agents.

Comprised of many DDQN networks with one per adversarial agent


"""

import math
import adversary.ddAdvAgent as ddAdvAgent
import numpy as np
class RandomAdvMaster():

    def __init__(self, adv_settings, network_setting):



        self.pre_train_steps = adv_settings.pre_train_steps
        self.action_per_agent = adv_settings.action_per_agent
        self.tau = adv_settings.tau
        self.discount_factor = adv_settings.discount_factor
        self.update_freq = adv_settings.update_freq
        self.batch_size = adv_settings.batch_size

        self.num_agents = network_setting.N_state



        self.states_per_agent = self.num_agents*7
        self.network_setting = network_setting 


        self.agents = []


        N_adv_state = self.num_agents*4
        for _ in range(self.num_agents):
            self.agents.append(ddAdvAgent.ddAdvAgent(N_adv_state, adv_settings))

        self.unassignedAgents = self.agents.copy() # hopefully we copy the references
        self.throttlerLeafDic = {}

    def __enter__(self):
        print("__enter__ RandomAdvMaster decentralised")
        for agent in self.agents:
            #agent.__enter__()
            #agent.sess = tf.Session()
            #agent.sess.run(agent.init)
            agent.__enter__()

    def __exit__(self, type, value, tb):
        print("\n\nmaster__exit__ called\n\n")
        for agent in self.agents:
            agent.__exit__(type, value, tb)

    def predict(self, state, total_steps, e):
        """
            only provide each agent with its corresponding state
            instead of combining the actions into a single action 
            lets use an array.

            Here we just calculate the % of traffic from capacity each agent produces

        """

        actions = []
        # print("\n\npredictions")
        for i in range(len(self.agents)):

            agentAction = self.agents[i].predict(state, total_steps, e)
            actions.append(agentAction)


        return actions

    def sendTraffic(self, actions):
        #given the actioons send the traffic
        for i in range(len(self.agents)):
            self.agents[i].sendTraffic(actions[i])

    def calc_reward(self, network_reward):
        # convert the network reward to the adversarial reward
        return 1 - network_reward



    def get_state(self):
        """ 
        Provide the bandwidth capacity for each agent,
        and bandwidth emmitted by each agent over last 3 steps
        last 3 
        """
        assert(len(self.prior_actions) == 3)
        
        state = self.bandwidths.copy() # start off with bandwidths
        for prior_action in self.prior_actions:
            state.extend(prior_action)

        return np.array(state)

    def initiate_episode(self):
        # here I assume that we know the number of designated attackers
        # The idea is to copy the same probabilty distribution as we had for
        # the normal version. This would be the closest mimic to the training.
        # Another idea is to use an alternate probablity distribution
        
        self.step_count = 0
        self.prior_actions = []
        for _ in range(3): #num past experiences
            self.prior_actions.append([0] * self.num_agents)
        self.bandwidths= [] # list of the traffic agent can emmit

        for i in range(len(self.agents)):
            self.agents[i].initiate_episode() # just calculating the bandwidths
            self.bandwidths.append(self.agents[i].illegal_traffic)
        # for i in range(len(attackers_per_host)):
        #     attackers = attackers_per_host[i]
        #     for _ in range(attackers):
        #         # repeat each number of attackers
        #         self.bandwidths[i] += self.min_bandwidth + np.random.rand()*(self.max_bandwidth - self.min_bandwidth)


    def update_past_state(self, actions):
        self.prior_actions.pop(0)
        self.prior_actions.append(actions)

    def update(self, last_state, last_actions, current_state, is_done, network_reward):
        # provide the update function to each individual state
        reward = self.calc_reward(network_reward)

        for i in range(len(self.agents)):
            agent = self.agents[i]
            last_action = last_actions[i]

            agent.update(last_state, last_action, current_state, is_done, reward)
        

        self.update_past_state(last_actions)

    def actionReplay(self, current_state, batch_size):
        # print(batch_size)
        # print(current_state)
        l = 0
        for i in range(len(self.agents)):
            agent = self.agents[i]

            l+= agent.actionReplay(current_state, batch_size)
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



    


    # The following code is abouot assigning leafs to agents

    def assignLeaf(self, leaf):
        # assign a leaf to an agent

        assert(not leaf in self.throttlerLeafDic.values())

        current_switch = leaf.destination_switch

        while(current_switch.is_filter==False):
            current_switch = current_switch.destination_links[0].destination_switch

        if not current_switch in self.throttlerLeafDic:
            self.throttlerLeafDic[current_switch] = self.unassignedAgents.pop()

        self.throttlerLeafDic[current_switch].addLeaf(leaf)













