#import requests
#import json
import numpy as np
#import math
#import copy
from enum import Enum
import pickle

import agent # i think this is the other folder but I dont think it would have access to this?

"""
#TODO
2) Implement nodes for realistic implementation
5) Do a close inspection of the state at the very start and run through to make sure the network is running right
6) Confirm rewards...might be incentive to accept everything
7) Simulate network milliseconds
#DONE
1) Created flexible adverseary
2) Seperate 'move_traffic' from 'get_state'
3) Convert drop_probabilities to dynamic
4) Implement a observation window

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

class Switch():
    def __init__(self, switch_id, is_filter):
        self.id = switch_id
        self.source_links = []
        self.destination_links = []
        self.attatched_hosts = []
        self.throttle_rate = 0
        
        self.legal_window = 0
        self.illegal_window = 0
        self.dropped_legal_window = 0
        self.dropped_illegal_window = 0

        self.legal_traffic = 0
        self.dropped_legal = 0
        self.illegal_traffic = 0
        self.dropped_illegal = 0

        self.new_legal = 0
        self.new_dropped_legal = 0
        self.new_illegal = 0
        self.new_dropped_illegal = 0

        self.is_filter = is_filter

    def sendTraffic(self):
        # an initial part of passing traffic along
        num_dests = len(self.destination_links)


        legal_pass = self.legal_traffic * (1 - self.throttle_rate)
        legal_dropped = self.legal_traffic * self.throttle_rate        
        # legal_pass = int(self.legal_traffic * (1-self.throttle_rate))
        # legal_dropped = self.legal_traffic - legal_pass

        illegal_pass = self.illegal_traffic * (1 - self.throttle_rate)
        illegal_dropped = self.illegal_traffic * self.throttle_rate
        # illegal_pass = int(self.illegal_traffic * (1 - self.throttle_rate)) 
        # illegal_dropped = self.illegal_traffic - illegal_pass

        # update all other switches with new traffic values
        for dest in self.destination_links:
            dest.destination_switch.new_legal += (legal_pass/num_dests)
            dest.destination_switch.new_dropped_legal += ((legal_dropped + self.dropped_legal)/num_dests)

            dest.destination_switch.new_illegal += (illegal_pass/num_dests)
            dest.destination_switch.new_dropped_illegal += ((illegal_dropped+ self.dropped_illegal)/num_dests)

    def updateSwitch(self):
        # update the traffic values
        self.legal_traffic = self.new_legal
        self.illegal_traffic = self.new_illegal
        self.dropped_legal = self.new_dropped_legal
        self.dropped_illegal = self.new_dropped_illegal

        # register switches interested in
        self.legal_window += self.legal_traffic
        self.illegal_window += self.illegal_traffic

        self.dropped_legal_window += self.dropped_legal
        self.dropped_illegal_window += self.dropped_illegal_window
        # reset new traffic values
        self.new_legal = 0
        self.new_illegal = 0
        self.new_dropped_legal = 0
        self.new_dropped_illegal = 0

    def resetWindow(self):
        self.legal_window=0
        self.illegal_window = 0
        self.dropped_legal_window = 0
        self.dropped_illegal_window = 0

    def getWindow(self):
        return self.legal_window + self.illegal_window

    def getImmediateState(self):
        return self.legal_traffic + self.illegal_traffic

    def setThrottle(self, throttle_rate):
        assert(self.is_filter)
        self.throttle_rate = throttle_rate

    def reset(self):
        self.legal_traffic = 0
        self.dropped_legal = 0
        self.illegal_traffic = 0
        self.dropped_illegal = 0
        self.new_legal = 0
        self.new_dropped_legal = 0
        self.new_illegal = 0
        self.new_dropped_illegal = 0
        self.resetWindow()

    def printSwitch(self):
       print("switch_id {0} | load {1} | window {2}".format(self.id, self.legal_traffic + self.illegal_traffic, self.getWindow()))

class link(object):
    id = -1
    source_node = None
    source_port = None
    source_switch = None # switch object
    destination_node = -1
    destination_port = -1
    destination_switch = None # switch object
    status = -1
    importance = -1
    bandwidth = -1


    def printLink(self):
        print("id: {0} | source_node {1} | source_port {2} | destination_node {3} | destination_port {4} | bandwidth {5}".format(\
            self.id, self.source_node, self.source_port, self.destination_node, self.destination_port, self.bandwidth))

class network(object):
    # def __init__(self, N_switch, N_action, N_state, action_per_throttler, host_sources, servers, filter_list, reward_overload, 
    #           rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
    #           legal_probability, upper_boundary, hostClass, max_epLength, f_link, SaveAttackEnum,
    #           save_attack, load_attack_path):

    #self.ITERATIONSBETEENACTION = 200 # with 10 ms delay, and throttle agent every 2 seconds, we see 200 messages passed in between
    def __init__(self, network_settings, reward_overload, adversary_class, max_epLength, load_attack_path = None, save_attack=False):
        



        self.iterations_between_action = network_settings.iterations_between_action# ideally set at 200
        self.host_sources = np.empty_like(network_settings.host_sources)
        self.host_sources[:] = network_settings.host_sources
        self.servers = np.empty_like(network_settings.servers)
        self.servers[:] = network_settings.servers # list of the servers. Usually [0]
        self.filter_list = network_settings.filters
        self.N_state = network_settings.N_state
        self.N_switch = network_settings.N_switch # number of nodes?
        self.N_action = network_settings.N_action
        self.N_server = len(self.servers)
        self.N_host = len(self.host_sources)
        self.N_filter = len(self.filter_list)
        self.action_per_throttler = network_settings.action_per_throttler # actions each host can take
        self.reward_overload = reward_overload
        self.rate_legal_low = (network_settings.rate_legal_low / self.iterations_between_action)
        self.rate_legal_high = (network_settings.rate_legal_high / self.iterations_between_action)
        self.rate_attack_low = (network_settings.rate_attack_low / self.iterations_between_action)
        self.rate_attack_high = (network_settings.rate_attack_high / self.iterations_between_action)
        
        self.legal_probability = network_settings.legal_probability # odds of host being an attacker
        self.upper_boundary = network_settings.upper_boundary
        self.hostClass = adversary_class
        self.topology = []
        self.max_epLength = max_epLength

        # specific to new network
        self.switches = [] # list of all switches, first one shouuld be attatched to server
        self.links = []
        self.hosts = []
        self.attack_record = [] # list of all attack stats, used if we're saving the attack

        # self.SaveAttackEnum = SaveAttackEnum
        self.save_attack = save_attack
        self.load_attack_path = load_attack_path
        self.initialise(network_settings.topologyFile)
        self.last_state = np.empty_like(self.get_state())


    def reset(self):
        if self.load_attack_path: # if we provide a file to oad from use it
            self.load_attacker()
        else:
            self.set_attackers()
        if self.save_attack:# is self.SaveAttackEnum.save:
            self.record_attackers()
        #self.set_rate()
        self.legitimate_all = 0
        self.legitimate_served = 0
        for i in range(self.N_switch):
            self.switches[i].reset()
            is_filter = i in self.filter_list
            if is_filter:
                self.switches[i].setThrottle(np.random.randint(0,self.action_per_throttler)/self.action_per_throttler)
        self.server_failures = 0

        #self.drop_probability.clear()


    def get_link(self, topology, f_link, v):
        with open(f_link) as f:
            count = 0
            for line in f:
                line = line.strip('\n')
                count += 1
                # Note I swapped dest/source from Yi as makes more sense for traffic going toward router
                dest_nd_id = int(line.split('-')[0])
                source_nd_id = int(line.split('-')[1])

                topology[source_nd_id][dest_nd_id] = v
                topology[dest_nd_id][source_nd_id] = v

            return count

    def set_attackers(self):
        # sets a random amount of attackers inbetween (but not inclusive) 0 and max
        # I think just replace this if you want to replicate attacks

        attackers = []
        assert self.N_host!=0 or self.N_host!=1 # to stop infinite loops
        while len(attackers) == 0 or len(attackers) == self.N_host:
        #do not allow "none/all attacker"
            attackers.clear()
            for i in range(self.N_host):
                if np.random.rand() >= self.legal_probability:
                    attackers.append(i)

        for i in range(len(self.hosts)):
            if i in attackers:
                self.hosts[i].reset(is_attacker=True)
            else:
               self.hosts[i].reset(is_attacker=False) 
     
    def record_attackers(self):
        details = []
        for host in self.hosts:
            details.append((host.is_attacker, host.traffic_rate))

        self.attack_record.append(details)


    def load_attacker(self):
        host_data = self.saved_attack.pop()
        #print(host_data)
        for i in range(len(host_data)):
            (is_attacker, traffic_rate) = host_data[i]
            self.hosts[i].setRate(is_attacker, traffic_rate)


    def get_state(self):
        # grab the state of the switches we're interested in
        state = []
        #print(self.filter_list)

        for i in self.filter_list:
            # self.switches[i].printSwitch()
            state.append(self.switches[i].getWindow())

        return state
        
    def move_traffic(self, time_step):
        # update the network


        for host in self.hosts:
            host.sendTraffic(time_step)

        for switch in self.switches:
            # ensure all traffic sent before we update
            switch.sendTraffic()

        for switch in self.switches:
            switch.updateSwitch()

    def set_drop_probability(self, action):

        for i in range(self.N_state):
            j = self.N_state - (i + 1) # start at one below host, end at 0
            divider = self.action_per_throttler**j

            switch_id = self.filter_list[i]
            drop_prob = int(action / divider)
            action = action - (drop_prob*divider)
            drop_prob /= self.action_per_throttler # to turn into a percentage
            self.switches[switch_id].setThrottle(drop_prob)

        assert(action==0) 

    def initialise(self, f_link):
        for i in range(self.N_switch):
            l = []
            for j in range(self.N_switch):
                l.append(-1)
            self.topology.append(l)

        n_lk = self.get_link(self.topology, f_link, 1)
        
        for i in range(self.N_switch):
            is_filter = i in self.filter_list
            self.switches.append(Switch(i, is_filter))

        
        for i in range(0, self.N_switch-1):
            for j in range(i, self.N_switch):
                if self.topology[i][j] != -1:
                    l = link()
                    l.id = len(self.links)
                    l.destination_switch = self.switches[i]
                    self.links.append(l)

                    self.switches[i].source_links.append(l)
                    self.switches[j].destination_links.append(l)                                    

        
        for i in self.host_sources:

            host = self.hostClass(self.switches[i], self.rate_attack_low, self.rate_attack_high,
                self.rate_legal_low, self.rate_legal_high, self.max_epLength)
            self.hosts.append(host)
        
        if self.load_attack_path:
            self.load_attacker_file()

        self.reset()

    """
    def virtual_action(self, action, prior_action, step_count):
        # if we want to test what the reward would be for an action without effecting the state
        # we do this by doing the action, then doing the prior action again

        self.step(action, step_count, False)
        r = self.calculate_reward()
        self.step(prior_action, step_count, False)
        return r
    """

    def calculate_reward(self):
        # currently if we're 1.1 times over we receive a punishment of -0.1, seems rather low. Maybe -1.5?        
        reward = 0.0

        legitimate_rate = self.switches[0].legal_window
        legitimate_rate_all = self.switches[0].legal_window + self.switches[0].dropped_legal_window
        attacker_rate = self.switches[0].illegal_window
        #assert((legitimate_rate+attacker_rate)==self.switches[0].getWindow())

        if legitimate_rate + attacker_rate > self.upper_boundary:
            #used to set the reward to "reward_overload" in this case, but didn't work well
           
            # print("\n\n\n negative reward")
            # print(self.upper_boundary)
            reward -= ((legitimate_rate + attacker_rate)/self.upper_boundary - 1.0)
            self.server_failures +=1
        else:
            if legitimate_rate_all != 0:
                reward += legitimate_rate/legitimate_rate_all
        
            self.legitimate_served += legitimate_rate
        
        self.legitimate_all += legitimate_rate_all

        return clip(-1, 1, reward)

    def step(self, action, step_count, update_last_state = True):
        # input the actions. Just sets drop probabilities at the moment
        # ideally i would move calculations here

        if update_last_state:
            self.last_state = self.get_state()

        for switch in self.switches:
            switch.resetWindow()
        
        self.set_drop_probability(action)
        for i in range(self.iterations_between_action): # each time delay is 10 ms, 10*200 = 2000 ms = 2 seconds
           self.move_traffic(step_count)


        #self.adversary.takeStep()
        # should pass the data along nodes

        # this is where we would update attack rates for NON-CONSTANT attacks

    def getLegitStats(self):
        # returns % of packets served in an episode
        # meant to be used at end of an epsisode
        if self.legitimate_all == 0:
            return (0, 0, 0)
        else:
            per = self.legitimate_served / self.legitimate_all
            return self.legitimate_served, self.legitimate_all, per, self.server_failures

    
    # def save_attacks(self):
    #     with open(self.load_attack_path, "wb") as f:
    #         print("saving the attack")
    #         pickle.dump(self.attack_record, f, pickle.HIGHEST_PROTOCOL)


    def load_attacker_file(self):
        with open(self.load_attack_path, 'rb') as f:
            print("opening saved attack")
            self.saved_attack = pickle.load(f) 
            #print("attack {0}".format(self.saved_attack))    

    def printState(self):
        for switch in self.switches:
            if switch.destination_links:
                dest = switch.destination_links[0].destination_switch.id
            else:
                dest = None
            print("id {0} | load {1} | window {2} | destination {3}".format(switch.id, switch.getImmediateState(), switch.getWindow(), dest))






