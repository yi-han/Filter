"""
Generic interface for many agents for adversary.

The structure allows a coordinated attacker to consist of many learning agents
This file acts as the central coordinating tool of IDA.

"""

import math
import numpy as np
import copy 
import agent.tileCoding as tileCoding
from network.utility import *
import adversary.genericMaster as genericMaster
class GenericAdvMaster(genericMaster.GenericAdvMaster):

    def __init__(self, adv_settings, network_setting, defender_path, defender):

        self.adv_settings = adv_settings
        self.num_adv_agents = adv_settings.num_adv_agents # number of adversarial agents
        self.num_agents = network_setting.N_state # number of defender agents
        # above 0 indicates the total number of agents
        # below 0 indicates the number of defenders each agent is responsible for
        if self.num_adv_agents < 0:
            self.num_adv_agents = -1 * self.num_adv_agents
            self.num_adv_agents = math.ceil(self.num_agents / self.num_adv_agents)        

        print("looking for last {0} seconds and {1} actions".format(adv_settings.prior_agent_seconds, adv_settings.prior_agent_seconds * defender.agent_settings.actions_per_second))
        assert(adv_settings.prior_agent_seconds % defender.agent_settings.actions_per_second == 0)
        self.prior_agent_actions = int(adv_settings.prior_agent_seconds * defender.agent_settings.actions_per_second) # number of actions by the defender we use in state
        self.prior_agent_deltas = int(adv_settings.prior_agent_delta_seconds * defender.agent_settings.actions_per_second)
        self.prior_adversary_actions = adv_settings.prior_adversary_actions # number of actions by advesary we use in state
        
        # Calculate the size of the state provided to IDA each step
        if self.adv_settings.prior_server_loads:
            self.server_loads = [0] * self.adv_settings.prior_server_loads
        N_adv_state = defender.num_agents*self.prior_agent_actions + (self.num_adv_agents * 1) + (self.num_adv_agents * self.prior_adversary_actions)# plus one due to bandwiths
        if adv_settings.packets_last_step:
            assert(1==2)
            # depreciated

        if self.adv_settings.include_indiv_hosts:
            # Include the packet potential of each Host in state
            N_adv_state += len(network_setting.host_sources)

        N_adv_state += self.prior_agent_deltas


        if self.adv_settings.include_legal_traffic:
            # Include the traffic potential of legal Hosts
            N_adv_state += self.num_adv_agents

        # Enables different representations of the prior server load
        N_adv_state += self.adv_settings.prior_server_loads
        N_adv_state += self.adv_settings.prior_server_percentages

        if self.adv_settings.indiv_host_info in [advHostInfoEnum.hostRoles, advHostInfoEnum.hostLoads, advHostInfoEnum.advLoads]:
            N_adv_state += len(network_setting.host_sources)

        if self.adv_settings.indiv_host_info == advHostInfoEnum.loadsAndRoles:
            N_adv_state += 2*len(network_setting.host_sources)

        self.adv_agents = []
        self.defender = defender
        self.defender_path = defender_path


        encoders = None


        # Now considers the existance of simultaneous learners and what information we include
        print("adv_stat size is {0}".format(N_adv_state))
        for _ in range(self.num_adv_agents):
            self.adv_agents.append(self.adv_settings.adv_agent_class(N_adv_state, adv_settings, encoders))
            if adv_settings.include_other_attackers:
                # If we want to include the moves of the attackers before it (turns actions into sequential)
                N_adv_state += 1
                if adv_settings.include_encoder:
                    encoders = copy.deepcopy(encoders) # copy it

                    encoders.append(advesary_move_encoding)

        self.all_leaves = [] # list of lists of leaves. Eventually grouped so each inner list corresponds to an adversarial agent


        self.name = adv_settings.name
        self.N_adv_state = N_adv_state


    def __enter__(self):
        print("__enter__ GenericAdvMaster decentralised")

        self.assignLeafs()

        for agent in self.adv_agents:
            # initiate each individual learner
            agent.__enter__()

    def __exit__(self, type, value, tb):
        print("\n\nmaster__exit__ called\n\n")
        for agent in self.adv_agents:
            agent.__exit__(type, value, tb)

    def predict(self, state, e, step, can_attack):
        """
            only provide each agent with its corresponding state
            instead of combining the actions into a single action 
            lets use an array.

            Here we just calculate the % of traffic from capacity each agent produces

        """

        # For allowing agents to see other agents moves for the same attack (for an IDA variant)
        if self.adv_settings.include_other_attackers:
            # we've already calculated the moves in this case
            return state[-1]


        actions = []
        for i in range(len(self.adv_agents)):
            # iterate through each learning agent and create attacking move
            agentAction = self.adv_agents[i].predict(state, e, can_attack)
            actions.append(agentAction)


        return actions







    def update_state(self, net):
        """ 
        Update the state to be provided to each learning agent

        

        """
        assert(len(self.prior_actions) == self.prior_adversary_actions)
        
        state = []
        state.extend(self.ill_bandwidths) # start off with ill_bandwidths

        if self.adv_settings.include_indiv_hosts:
            assert(1==2) # obsolete
            state.extend(self.ill_bandwidth_by_host)

        # host information:
        state.extend(self.host_info)


        for prior_action in self.prior_actions:
            state.extend(prior_action)


        if self.prior_agent_actions>0:
            # capture past predictions for learning
            for past_prediction in self.defender.past_predictions[-self.prior_agent_actions:]:
                state.extend(past_prediction)


        # sort of a hack. Do the prediction here as the move is done simultaneously 
        if self.adv_settings.include_other_attackers:
            # we disabled the ability to see other agents moves
            assert(1==2)


        if self.prior_agent_deltas:
            # update list of previous moves by agents
            last_changes = self.defender.past_moves[(-1*self.prior_agent_deltas):]
            for change in last_changes:
                state.extend(change) 

        if self.adv_settings.prior_server_loads:
            latest_load = net.switches[0].get_load()
            self.server_loads.pop(0)
            self.server_loads.append(latest_load)
            state.extend(self.server_loads)

        if self.adv_settings.include_legal_traffic:
            state.extend(self.leg_bandwidths)
        

        if(len(state)!=self.N_adv_state):
            print(len(state))
            print(self.N_adv_state)

            assert(1==2)

        self.current_state = np.array(state)

    def get_state(self):
        return self.current_state

    def extract_state(self, combined_state, i):
        if self.adv_settings.include_other_attackers:
            assert(1==2)
            return combined_state[i]
        else:
            # normal
            return combined_state


    def initiate_episode(self, episode_number):
        # here I assume that we know the number of designated attackers


        super().initiate_episode()

        self.step_count = 0
        self.prior_actions = []
        for _ in range(self.prior_adversary_actions): #num past experiences
            self.prior_actions.append([0] * self.num_adv_agents)
        self.ill_bandwidths= [] # list of the traffic agent can emmit
        self.ill_bandwidth_by_host = [] # list of ill_bandwidths of every single host
        self.host_info = [] # information about the host to include (done at the handler level)
        self.leg_bandwidths = [] # amount of legal traffic for each host
        for i in range(len(self.adv_agents)):
            self.adv_agents[i].initiate_episode() # just calculating the ill_bandwidths
            self.ill_bandwidths.append(self.adv_agents[i].illegal_traffic)
            self.leg_bandwidths.append(self.adv_agents[i].legal_traffic)
            self.ill_bandwidth_by_host.extend(self.adv_agents[i].illegal_traffic_by_host)
            self.host_info.extend(self.adv_agents[i].get_host_info(self.adv_settings.indiv_host_info))
        

        if self.adv_settings.prior_server_loads:

            for i in range(len(self.server_loads)):
                self.server_loads[i] = 0

    def update_past_state(self, actions):
        self.prior_actions.pop(0)
        self.prior_actions.append(actions)

    def update(self, last_state, last_actions, current_state, is_done, reward, next_actions):
        # initiate update on each learning agent
        for i in range(len(self.adv_agents)):
            agent = self.adv_agents[i]
            last_action = last_actions[i]
            next_action = next_actions[i]
            t_last_state = self.extract_state(last_state, i)
            t_current_state = self.extract_state(current_state, i)

            agent.update(t_last_state, last_action, t_current_state, is_done, reward, next_action)
        

        # self.update_past_state(last_actions)

    def actionReplay(self, current_state, batch_size):
        # when the learning happens
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



    


    # The following code is about assigning leafs to agents
    # Structurally leaves represent individual nodes which may be Hosts that send traffic to the network
    # The attacker python class serves a dual purpose of calculating attacker move and sending all traffic

    def addLeaf(self, leaf):
        # add the leaf to the set of leaves we have to assign

        # sanity check for duplication
        assert(not [leaf] in self.all_leaves)
        leaf.current_position = leaf.destination_switch
        # # leader is used for grouping the leaves together.
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












