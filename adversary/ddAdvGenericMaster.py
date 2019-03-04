"""
Generic interface for many agents for adversary.
We assign the potentials for each agent randomally each episode
as opposed to using another agent to coordinate the agents.

Comprised of many DDQN networks with one per adversarial agent


"""

import math
#import adversary.ddAdvGenericAgent as ddGenAgent
import numpy as np
import copy 
import agent.tileCoding as tileCoding
from network.utility import *

class GenericAdvMaster():

    def __init__(self, adv_settings, network_setting, defender_path, defender):

        self.adv_settings = adv_settings
        self.num_adv_agents = adv_settings.num_adv_agents # number of adversarial agents
        self.num_agents = network_setting.N_state # number of defender agents
        # above 0 inidicates the total number of agents
        # below 0 indicates the number of defenders each agent is responsible for
        if self.num_adv_agents < 0:
            self.num_adv_agents = -1 * self.num_adv_agents
            self.num_adv_agents = math.ceil(self.num_agents / self.num_adv_agents)        


        self.prior_agent_actions = adv_settings.prior_agent_actions # number of actions by the defender we use in state
        self.prior_adversary_actions = adv_settings.prior_adversary_actions # number of actions by advesary we use in state
        self.packets_last_step = adv_settings.packets_last_step
        
        N_adv_state = defender.num_predictions*self.prior_agent_actions + (self.num_adv_agents * 1) + (self.num_adv_agents * self.prior_adversary_actions)# plus one due to bandwiths
        if self.packets_last_step:
            N_adv_state += 1

        if self.adv_settings.include_indiv_hosts:
            N_adv_state += len(network_setting.host_sources)

        N_adv_state += self.adv_settings.prior_agent_delta_moves

        self.adv_agents = []
        self.defender = defender
        self.defender_path = defender_path

        if adv_settings.include_encoder:
            maxThrottlerBandwidth = len(network_setting.host_sources)*network_setting.rate_attack_high
            bandwidth_tiles = min(maxThrottlerBandwidth,100) # cap off our max bandwidth at 100 tiles. More than enough
            bandwidth_tilings = 8

            print("my detected max bandwidth is {0}".format(maxThrottlerBandwidth))
            bandwidth_encoding = tileCoding.myTileInterface(maxThrottlerBandwidth, bandwidth_tiles, bandwidth_tilings)

            max_agent_value, agent_tiles, agent_tilings = defender.get_max_agent_value()
            agent_move_encoding = tileCoding.myTileInterface(max_agent_value, agent_tiles, agent_tilings)
            advesary_move_encoding = tileCoding.myTileInterface(adv_settings.action_per_agent, adv_settings.action_per_agent, agent_tilings)


            packets_last_step_encoding = tileCoding.myTileInterface(1.001, 11, 8)

            if self.adv_settings.prior_agent_delta_moves:
                max_delta_value, delta_tiles, delta_tilings = defender.get_move_delta_values()

                prior_agent_delta_move_encoder = tileCoding.myTileInterface(max_delta_value, delta_tiles, delta_tilings)

            encoders = [bandwidth_encoding]*self.num_adv_agents # bandwidht each advAgent has
            if self.prior_adversary_actions:
                # move each advesary has made
                encoders.extend([advesary_move_encoding]*(self.prior_adversary_actions*self.num_adv_agents)) 
            if self.prior_agent_actions:
                # move the defender made
                encoders.extend([agent_move_encoding]*(self.prior_agent_actions*defender.num_predictions)) 
            if self.packets_last_step:
                # record the percentage of packets successfully made it to the server last round
                encoders.extend([packets_last_step_encoding]) 

            if self.adv_settings.prior_agent_delta_moves:
                encoders.extend(([prior_agent_delta_move_encoder]*self.adv_settings.prior_agent_delta_moves))
            print(len(encoders))
            print(N_adv_state)

            assert(len(encoders)==N_adv_state)
        else:
            encoders = None



        print("adv_stat size is {0}".format(N_adv_state))
        for _ in range(self.num_adv_agents):
            self.adv_agents.append(self.adv_settings.adv_agent_class(N_adv_state, adv_settings, encoders))
            if adv_settings.include_other_attackers:
                # If we want to include the moves of the attackers before it
                N_adv_state += 1
                if adv_settings.include_encoder:
                    encoders = copy.deepcopy(encoders) # copy it

                    encoders.append(advesary_move_encoding)

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

    def predict(self, state, e, step):
        """
            only provide each agent with its corresponding state
            instead of combining the actions into a single action 
            lets use an array.

            Here we just calculate the % of traffic from capacity each agent produces

        """
        if self.adv_settings.include_other_attackers:
            # we've already calculated the moves in this case
            return state[-1]


        actions = []
        # print("\n\npredictions")
        for i in range(len(self.adv_agents)):

            agentAction = self.adv_agents[i].predict(state, e, step)
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



    def get_state(self, net, e, step, last_reward):
        """ 
        Provide the bandwidth capacity for each agent,
        and bandwidth emmitted by each agent over last 3 steps
        last 3 

        pack_per_last_action is 
        """
        assert(len(self.prior_actions) == self.prior_adversary_actions)
        
        # print("\n\n")
        state = list(map(lambda x: KbToMb(x), self.bandwidths)) # start off with bandwidths
        # print(state)
        #print(self.prior_actions)
        #print("actions done")
        # state.extend(self.prior_actions)
        if self.adv_settings.include_indiv_hosts:
            state.extend(self.bandwidth_by_host)

        for prior_action in self.prior_actions:
            state.extend(prior_action)

        # pThrottles = []

        if self.prior_agent_actions>0:
            
            for past_prediction in self.defender.past_predictions[-self.prior_agent_actions:]:
                state.extend(past_prediction)

        if self.packets_last_step:
            percentage_packets = max(last_reward, 0) # remove negative reward
            state.append(percentage_packets)
        # sort of a hack. Do the prediction here as the move is done simultaneously 
        if self.adv_settings.include_other_attackers:

            combined_state = []
            associated_actions = []
            for i in range(len(self.adv_agents)):
                combined_state.append(copy.deepcopy(state))
                associated_action = self.adv_agents[i].predict(state,e, step)
                state.append(associated_action)
                associated_actions.append(associated_action)
            # record the actions in the state variable
            combined_state.append(associated_actions)
            return combined_state

        if self.adv_settings.prior_agent_delta_moves:
            last_changes = self.defender.past_moves[(-1*self.adv_settings.prior_agent_delta_moves):]
            for change in last_changes:
                state.extend(change) 
        return np.array(state)

    def extract_state(self, combined_state, i):
        if self.adv_settings.include_other_attackers:
            return combined_state[i]
        else:
            # normal
            return combined_state


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
        self.bandwidth_by_host = [] # list of bandwidths of every single host
        for i in range(len(self.adv_agents)):
            self.adv_agents[i].initiate_episode() # just calculating the bandwidths
            self.bandwidths.append(self.adv_agents[i].illegal_traffic)
            self.bandwidth_by_host.extend(self.adv_agents[i].illegal_traffic_by_host)
        # for i in range(len(attackers_per_host)):
        #     attackers = attackers_per_host[i]
        #     for _ in range(attackers):
        #         # repeat each number of attackers
        #         self.bandwidths[i] += self.min_bandwidth + np.random.rand()*(self.max_bandwidth - self.min_bandwidth)


    def update_past_state(self, actions):
        self.prior_actions.pop(0)
        self.prior_actions.append(actions)

    def update(self, last_state, last_actions, current_state, is_done, reward, step, next_actions):
        # provide the update function to each individual state
        # reward = self.calc_reward(network_reward)
        for i in range(len(self.adv_agents)):
            agent = self.adv_agents[i]
            last_action = last_actions[i]
            next_action = next_actions[i]
            t_last_state = self.extract_state(last_state, i)
            t_current_state = self.extract_state(current_state, i)

            agent.update(t_last_state, last_action, t_current_state, is_done, reward, step, next_action)
        

        # self.update_past_state(last_actions)

    def actionReplay(self, current_state, batch_size):

        l = 0
        for i in range(len(self.adv_agents)):
            agent = self.adv_agents[i]
            t_state = self.extract_state(current_state, i)
            l+= agent.actionReplay(t_state, batch_size)
        return l

    def loadModel(self, load_path, prefix):
        # note we are going to use the index of the array as an id
        print("loading all models")
        for i in range(len(self.adv_agents)):
            individual_path = load_path+'/{0}Adv-{1}'.format(i, prefix)
            checkpoint = self.adv_agents[i].loadModel(individual_path)
        return checkpoint

    def saveModel(self,load_path, interation, prefix):
        for i in range(len(self.adv_agents)):
            individual_path = load_path+'/{0}Adv-{1}'.format(i, prefix)
            self.adv_agents[i].saveModel(individual_path, interation)


    def getPath(self):
        return "{0}/{1}".format(self.defender_path,self.name)

    def reset(self):
        assert(1==2) # dont think we use this
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












