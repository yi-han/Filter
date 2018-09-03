import requests, json
import numpy as np
import math
import copy

import agent # i think this is the other folder but I dont think it would have access to this?

"""
#TODO
2) Remove all hard coded stuff
2) Implement nodes for realistic implementation
4) Implement a observation window
5) Do a close inspection of the state at the very start and run through to make sure the network is running right

#DONE
1) Created flexible adverseary
2) Seperate 'next_state' from 'get_state'
3) Convert drop_probabilities to dynamic

#OTHER
1) Note whilst calcPercentage is a part of getReward it doesn't evaluate for the first step (so not full)

"""

def clip(min_value, max_value, value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value

def deep_copy_state(state):
    state_copy = np.empty_like(state)
    state_copy[:] = state
    return state_copy

class link(object):
    id = -1
    source_node = -1
    source_port = -1
    destination_node = -1
    destination_port = -1
    status = -1
    importance = -1
    bandwidth = -1

class network(object):
    def __init__(self, N_switch, N_action, N_state, action_per_agent, hosts, servers, filters, reward_overload, 
              rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
              legal_probability, upper_boundary, adv, max_epLength, f_link):
        self.hosts = np.empty_like(hosts)
        self.hosts[:] = hosts
        self.servers = np.empty_like(servers)
        self.servers[:] = servers
        self.filters = np.empty_like(filters)
        self.filters[:] = filters
        self.attackers = [] # id corresponds to the host attatched

        self.N_state = N_state
        self.N_switch = N_switch
        self.N_action = N_action
        self.N_server = len(self.servers)
        self.N_host = len(self.hosts)
        self.N_filter = len(self.filters)
        self.action_per_agent = action_per_agent # actions each host can take
        
        self.reward_overload = reward_overload
        
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high
        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        
        self.legal_probability = legal_probability # odds of host being an attacker
        self.upper_boundary = upper_boundary
        self.adv = adv
        self.topology = []
        self.links = []
        self.filter_host = {}
        self.current_state = [] #aggregate traffic rate
        self.drop_probability = [] # percentage of traffic stopping
        self.max_epLength = max_epLength

        self.initialise(f_link)
        self.last_state = np.empty_like(self.current_state)


    def reset(self):
        self.set_attackers()
        #self.set_rate()
        
        self.adversary = self.adv(self.N_host, self.attackers, self.rate_attack_low, self.rate_attack_high, 
            self.rate_legal_low, self.rate_legal_high, self.max_epLength)

        
        self.legitimate_served = 0
        self.legitimate_all = 0
        self.is_functional = True

        self.drop_probability.clear()
        for i in range(self.N_filter):
            #TODO
            self.drop_probability.append(np.random.randint(0,self.action_per_agent)/self.action_per_agent)

        self.current_state = [0.0] * self.N_filter

    def get_link(self, topology, f_link, v):
        with open(f_link) as f:
            count = 0
            for line in f:
                line = line.strip('\n')
                count += 1
                source_nd_id = int(line.split('-')[0])
                dest_nd_id = int(line.split('-')[1])

                topology[source_nd_id][dest_nd_id] = v
                topology[dest_nd_id][source_nd_id] = v

            return count

    def set_attackers(self):
        # sets a random amount of attackers inbetween (but not inclusive) 0 and max
        self.attackers.clear()

        assert self.N_host!=0 or self.N_host!=1 # to stop infinite loops

        while len(self.attackers) == 0 or len(self.attackers) == self.N_host:
        #do not allow "none/all attacker"
            self.attackers.clear()
            for i in range(self.N_host):
                if np.random.rand() >= self.legal_probability:
                    self.attackers.append(i)
        
    def get_state(self):
        return self.current_state
        

    
    def next_state(self):
        self.last_state[:] = self.current_state
        self.current_state.clear()        

        for i in range(self.N_filter):
            self.current_state.append(0)

            for j in self.filter_host[self.filters[i]]:
                
                self.current_state[i] += self.adversary.getHostRate()[j]
        
        return self.current_state        

    def set_drop_probability(self, action):

        for i in range(self.N_state):
            j = self.N_state - (i + 1) # start at one below host, end at 0
            divider = self.action_per_agent**j

            self.drop_probability[i] = int(action / divider)
            action = action - (self.drop_probability[i]*divider)
            self.drop_probability[i] /= self.action_per_agent # to turn into a percentage


        
        assert(action==0) 
        return self.drop_probability

    def initialise(self, f_link):
        for i in range(self.N_switch):
            l = []
            for j in range(self.N_switch):
                l.append(-1)
            self.topology.append(l)

        n_lk = self.get_link(self.topology, f_link, 1)
        
        #initialise links
        for i in range(self.N_switch-1):
            for j in range(i+1, self.N_switch):
                if self.topology[i][j] != -1:
                    l = link()
                    l.id = len(self.links)
                    l.source_node = i
                    l.destination_node = j
                    l.status = self.topology[i][j]
                    l.importance = 0

                    self.links.append(l)

        #TODO
        #hard-coded for now
        #a dict of {filter_ID:[Ids of hosts that are connected to the filter]}
        #self.filter_host.update({5:[0, 1, 2]})
        

        ### Jeremy, temporarily removed bottom two
        self.filter_host.update({5:[0, 1, 2]})
        self.filter_host.update({6:[3]})
        self.filter_host.update({9:[4, 5]})
        
        self.reset()

    def calculate_reward(self):
        
        reward = 0.0

        legitimate_rate = 0.0
        legitimate_rate_all = 0.0
        attacker_rate = 0.0

        for i in range(self.N_filter):
            for j in self.filter_host[self.filters[i]]:
                if j not in self.attackers:
                    legitimate_rate += self.adversary.getHostRate()[j] * (1-self.drop_probability[i])
                    legitimate_rate_all += self.adversary.getHostRate()[j]

                else:
                    attacker_rate += self.adversary.getHostRate()[j] * (1-self.drop_probability[i])

        if legitimate_rate + attacker_rate > self.upper_boundary:
            #used to set the reward to "reward_overload" in this case, but didn't work well
            reward -= ((legitimate_rate + attacker_rate)/self.upper_boundary - 1.0)
            self.is_functional = False
        else:
            reward += legitimate_rate/legitimate_rate_all
        
        # metrics for evaluation if we want
        if self.is_functional:
            # once incapacitated the server no longer can accept any more requests
            self.legitimate_served += legitimate_rate
        self.legitimate_all += legitimate_rate_all

        return clip(-1, 1, reward)

    def step(self, action, step):
        # input the actions. Just sets drop probabilities at the moment
        # ideally i would move calculations here
        #print("State: {0}".format(self.current_state))
        #print("Drop Prob are {0}".format(self.drop_probability))

        self.set_drop_probability(action)
        self.next_state()
        self.adversary.takeStep()
        # should pass the data along nodes

        # this is where we would update attack rates for NON-CONSTANT attacks

    def getLegitStats(self):
        # returns % of packets served in an episode
        # assumes if server has failed then no further packets were received
        # meant to be used at end of an epsisode
        per = self.legitimate_served / self.legitimate_all
        return self.legitimate_served, self.legitimate_all, per





