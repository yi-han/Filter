import requests, json
import numpy as np
import math
import copy

import agent # i think this is the other folder but I dont think it would have access to this?

"""
#TODO

0) Remove the whole MAX_STEP or 'd' from this, should be handled by experiment
1) Either allow fetching state without updating network or fix other code not to call for state so often
2) Convert drop_probabilities to dynamic
3) I'm confident that the calculation of state is incorrect
4) Note whilst calcPercentage is a part of getReward it doesn't evaluate for the first step (so not full)
"""


MAX_STEP = 30




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
    def __init__(self, N_switch, N_action, hosts, servers, filters, reward_overload, 
              rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
              legal_probability, upper_boundary, f_link):
        self.hosts = np.empty_like(hosts)
        self.hosts[:] = hosts
        self.servers = np.empty_like(servers)
        self.servers[:] = servers
        self.filters = np.empty_like(filters)
        self.filters[:] = filters
        self.attackers = []

        self.N_switch = N_switch
        self.N_action = N_action
        self.N_server = len(self.servers)
        self.N_host = len(self.hosts)
        self.N_filter = len(self.filters)
        
        self.reward_overload = reward_overload
        
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high
        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        
        self.legal_probability = legal_probability
        self.upper_boundary = upper_boundary
        
        self.topology = []
        self.links = []
        
        self.host_rate = []
        self.filter_host = {}
        self.current_state = [] #aggregate traffic rate
        self.drop_probability = []
        self.initialise(f_link)
        self.last_state = np.empty_like(self.current_state)

        # for evaluation
        self.legitimate_served = 0
        self.legitimate_all = 0
        self.is_functional = True

    def reset(self):
        self.set_attackers()
        self.set_rate()
        
        self.legitimate_served = 0
        self.legitimate_all = 0
        self.is_functional = True

        self.drop_probability.clear()
        for i in range(self.N_filter):
            #TODO
            self.drop_probability.append(np.random.randint(0,10)/10)

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
        self.attackers.clear()

        while len(self.attackers) == 0 or len(self.attackers) == self.N_host:
        #do not allow "none/all attacker"
            self.attackers.clear()
            for i in range(self.N_host):
                if np.random.rand() >= self.legal_probability:
                    self.attackers.append(i)
                
    def set_rate(self):
        self.host_rate.clear()
        for i in range(self.N_host):
            if i in self.attackers:
                self.host_rate.append(self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low))
            else:
                self.host_rate.append(self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low))
                
    def get_state(self):
        self.last_state[:] = self.current_state
        self.current_state.clear()
        
        for i in range(self.N_filter):
            self.current_state.append(0)

            for j in self.filter_host[self.filters[i]]:
                
                self.current_state[i] += self.host_rate[j]
        
        return self.current_state
    
    def set_drop_probability(self, action):
        #TODO
        #The implementation below only works for the current setup

        # self.drop_probability[0] = int(action)/10

        
        # Implementation for 3
        self.drop_probability[0] = int(action/100)
        self.drop_probability[1] = int((action - self.drop_probability[0]*100)/10)
        self.drop_probability[2] = int(action - self.drop_probability[0]*100 - self.drop_probability[1]*10)
        
        self.drop_probability[0] /= 10
        self.drop_probability[1] /= 10
        self.drop_probability[2] /= 10
        

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

    def calculate_reward(self, d, step):
        # not sure why we would take in d if we set it regardless
        if step < MAX_STEP:
            d = False
        else:
            d = True
        
        reward = 0.0

        legitimate_rate = 0.0
        legitimate_rate_all = 0.0
        attacker_rate = 0.0

        for i in range(self.N_filter):
            for j in self.filter_host[self.filters[i]]:
                if j not in self.attackers:
                    legitimate_rate += self.host_rate[j] * (1-self.drop_probability[i])
                    legitimate_rate_all += self.host_rate[j]

                else:
                    attacker_rate += self.host_rate[j] * (1-self.drop_probability[i])

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

        return d, clip(-1, 1, reward)

    def step(self, action):
        self.set_drop_probability(action)

    def getLegitStats(self):
        # returns % of packets served in an episode
        # assumes if server has failed then no further packets were received
        # meant to be used at end of an epsisode
        per = self.legitimate_served / self.legitimate_all
        return self.legitimate_served, self.legitimate_all, per





