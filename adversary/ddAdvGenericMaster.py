"""
Generic interface for many agents for adversary.
We assign the potentials for each agent randomally each episode
as opposed to using another agent to coordinate the agents.

Comprised of many DDQN networks with one per adversarial agent


"""

import math
import adversary.ddAdvGenericAgent as ddGenAgent
import numpy as np
class GenericAdvMaster():

    def __init__(self, adv_settings, network_setting, defender_path):

        self.num_adv_agents = adv_settings.num_adv_agents # number of adversarial agents
        self.num_agents = network_setting.N_state # number of defender agents

        # above 0 inidicates the total number of agents
        # below 0 indicates the number of defenders each agent is responsible for
        if self.num_adv_agents < 0:
            self.num_adv_agents = -1 * self.num_adv_agents
            self.num_adv_agents = math.ceil(self.num_agents / self.num_adv_agents)        


        self.prior_agent_actions = adv_settings.prior_agent_actions # number of actions by the defender we use in state
        self.prior_adversary_actions = adv_settings.prior_adversary_actions # number of actions by advesary we use in state




        N_adv_state = self.num_agents*self.prior_agent_actions+ self.num_adv_agents * (1 + self.prior_adversary_actions)# plus one due to bandwiths


        self.adv_agents = []
        self.defender_path = defender_path

        #N_adv_state = self.num_agents*7
        print("adv_stat size is {0}".format(N_adv_state))
        for _ in range(self.num_adv_agents):
            self.adv_agents.append(ddGenAgent.ddGenAgent(N_adv_state, adv_settings))

        self.all_leaves = [] # list of lists of leaves. Eventually grouped so each inner list corresponds to an adversarial agent
        #self.unassignedAgents = self.adv_agents.copy() # hopefully we copy the references
        #self.throttlerLeafDic = {}

        self.name = adv_settings.name

    def __enter__(self):
        print("__enter__ GenericAdvMaster decentralised")

        self.assignLeafs()

        for agent in self.adv_agents:
            #agent.__enter__()
            #agent.sess = tf.Session()
            #agent.sess.run(agent.init)
            agent.__enter__()

    def __exit__(self, type, value, tb):
        print("\n\nmaster__exit__ called\n\n")
        for agent in self.adv_agents:
            agent.__exit__(type, value, tb)

    def predict(self, state, e):
        """
            only provide each agent with its corresponding state
            instead of combining the actions into a single action 
            lets use an array.

            Here we just calculate the % of traffic from capacity each agent produces

        """

        actions = []
        # print("\n\npredictions")
        for i in range(len(self.adv_agents)):

            agentAction = self.adv_agents[i].predict(state, e)
            actions.append(agentAction)


        return actions

    def sendTraffic(self, actions):
        #given the actioons send the traffic
        for i in range(len(self.adv_agents)):
            self.adv_agents[i].sendTraffic(actions[i])

    def calc_reward(self, network_reward):
        # convert the network reward to the adversarial reward
        if network_reward<0:
            return 1
        else:
            return 1-network_reward



    def get_state(self, net):
        """ 
        Provide the bandwidth capacity for each agent,
        and bandwidth emmitted by each agent over last 3 steps
        last 3 
        """
        assert(len(self.prior_actions) == 3)
        
        # print("\n\n")
        state = self.bandwidths.copy() # start off with bandwidths
        # print(state)
        #print(self.prior_actions)
        #print("actions done")
        # state.extend(self.prior_actions)
        for prior_action in self.prior_actions:
            
            state.extend(prior_action)

        # pThrottles = []
        for throttler in net.throttlers:
            state.extend(throttler.past_throttles[-self.prior_agent_actions:])
        #     pThrottles.append(throttler.past_throttles)
        # print(pThrottles)
        # print(state)
        return np.array(state)

    def initiate_episode(self):
        # here I assume that we know the number of designated attackers
        # The idea is to copy the same probabilty distribution as we had for
        # the normal version. This would be the closest mimic to the training.
        # Another idea is to use an alternate probablity distribution
        



        self.step_count = 0
        self.prior_actions = []
        for _ in range(self.prior_adversary_actions): #num past experiences
            self.prior_actions.append([0] * self.num_adv_agents)
        self.bandwidths= [] # list of the traffic agent can emmit

        for i in range(len(self.adv_agents)):
            self.adv_agents[i].initiate_episode() # just calculating the bandwidths
            self.bandwidths.append(self.adv_agents[i].illegal_traffic)
        # for i in range(len(attackers_per_host)):
        #     attackers = attackers_per_host[i]
        #     for _ in range(attackers):
        #         # repeat each number of attackers
        #         self.bandwidths[i] += self.min_bandwidth + np.random.rand()*(self.max_bandwidth - self.min_bandwidth)


    def update_past_state(self, actions):
        self.prior_actions.pop(0)
        self.prior_actions.append(actions)

    def update(self, last_state, last_actions, current_state, is_done, reward):
        # provide the update function to each individual state
        # reward = self.calc_reward(network_reward)
        for i in range(len(self.adv_agents)):
            agent = self.adv_agents[i]
            last_action = last_actions[i]

            agent.update(last_state, last_action, current_state, is_done, reward)
        

        # self.update_past_state(last_actions)

    def actionReplay(self, current_state, batch_size):
        # print(batch_size)
        # print(current_state)
        l = 0
        for i in range(len(self.adv_agents)):
            agent = self.adv_agents[i]

            l+= agent.actionReplay(current_state, batch_size)
        return l

    def loadModel(self, load_path, prefix):
        # note we are going to use the index of the array as an id
        print("loading all models")
        for i in range(len(self.adv_agents)):
            individual_path = load_path+'/{0}Adv-{1}'.format(i, prefix)
            self.adv_agents[i].loadModel(individual_path)

    def saveModel(self,load_path, interation, prefix):
        for i in range(len(self.adv_agents)):
            individual_path = load_path+'/{0}Adv-{1}'.format(i, prefix)
            self.adv_agents[i].saveModel(individual_path, interation)


    def getPath(self):
        return "{0}/{1}".format(self.defender_path,self.name)

    def reset(self):
        for agent in self.adv_agents:
            agent.reset()



    


    # The following code is abouot assigning leafs to agents

    def addLeaf(self, leaf):
        # add the leaf to the set of leaves we have to assign

        # sanity check
        assert(not [leaf] in self.all_leaves)
        leaf.current_position = leaf.destination_switch
        # # leader is used for grouping the leaves together.
        # # use 
        self.all_leaves.append([leaf])


    def assignLeafs(self):
        """
        Each switch we encounter set a current leader. This ensures past ones catch up and order of priority
        """

        # assign each leaf to an advesarial agent

        k = 0

        switches_seen = {}
        while(len(self.all_leaves)>self.num_adv_agents):
            # keep going until we have as many sets as adversarial agents
            if k >= len(self.all_leaves):
                k = 0
            print("current {0} leaves | {1} agent | {2} k ".format(len(self.all_leaves), self.num_adv_agents, k))


            current_set = self.all_leaves[k]
            leader = current_set[0]

            if leader.current_position in switches_seen:
                associated_set = switches_seen[leader.current_position]
                self.all_leaves.remove(current_set)
                self.all_leaves.remove(associated_set)
                associated_set.extend(current_set)
                self.all_leaves.insert(0, associated_set)

                # remove all traces of this set
                for key in switches_seen:
                    if switches_seen[key]==current_set:
                        switches_seen[key] = associated_set
            else:
                switches_seen[leader.current_position]=current_set
                if leader.current_position.id !=0:
                    # skip as at server
                    leader.current_position = current_set[0].current_position.destination_links[0].destination_switch
                k += 1                
        # sanity check
        assert(len(self.all_leaves)==self.num_adv_agents)
        for i in range(self.num_adv_agents):
            self.adv_agents[i].addLeaves(self.all_leaves[i])
            print("adding {0} leaves to {1}".format(len(self.all_leaves[i]), i))












