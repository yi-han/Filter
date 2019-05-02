#import requests
#import json
import numpy as np
import math
#import copy
import pickle
from mapsAndSettings import stateRepresentationEnum
from mapsAndSettings import AGENT_REWARD_ENUM
from network.utility import *
#import agent # i think this is the other folder but I dont think it would have access to this?

"""
#TODO
5) Do a close inspection of the state at the very start and run through to make sure the network is running right
6) Confirm rewards...might be incentive to accept everything
7) Simulate network milliseconds
#DONE

if self.adversarialAgent != None:
self.adversarialAgent 1) Cr

eated flexible adversary
2) Seperate 'move_traffic' from 'get_state'
3) Convert drop_probabilities to dynamic
4) Implement a observation window
2) Implement nodes for realistic implementation

#OTHER
1) Note whilst calcPercentage is a part of getReward it doesn't evaluate for the first step (so not full)

"""





class Switch():
    def __init__(self, switch_id, is_filter, representation, defender_settings, iterations_between_second, bucket_capacity):
        """
        history_size: The number of things to remember

        """


        self.id = switch_id # id
        self.source_links = [] # places sending traffic to switch
        self.destination_links = [] # where traffic is getting sent
        self.attatched_hosts = [] # used for network_quick, quick access for hosts attatched to this 
        self.throttle_rate = -1 # the throttling rate for the specific switch
        self.memory = iterations_between_second * 2 # how much to remember. 2 seconds worth of data


        self.stateSwitches = [] # list of objects we use for state. If just self it shows only load at self

        self.representation = representation

        self.is_filter = is_filter
        if defender_settings.has_bucket and is_filter:
            # initiate a bucket
            self.bucket = defender_settings.bucket_class(iterations_between_second, bucket_capacity) #Bucket(iterations_between_second, bucket_capacity)
        else:
            self.bucket = None
        self.legal_segment = [0] * self.memory # over the last window, how much legal traffic has passed
        self.illegal_segment = [0] * self.memory # over the last window, how much illegal traffic has passed
        self.dropped_legal_segment = [0] * self.memory# how much legal traffic have we dropped over the last window
        self.dropped_illegal_segment = [0] * self.memory # over last window, how much illegal traffic has passed
     
        self.reset()

        self.delay = 0 # the delay for implementing a throttle based on maximum communication
    def sendTraffic(self):
        # an initial part of passing traffic along


        if self.is_filter:
            if self.iterations_since_throttle == self.delay and self.next_throttle != None:
                self.throttle_rate = self.next_throttle
                if self.bucket and self.is_filter:
                    # testing out new bucket approach
                    self.bucket.update_throttle_rate(self.throttle_rate, self.get_load())
                self.next_throttle = None
            # print("delay {0} throttle {1}".format(self.delay - self.iterations_since_throttle, self.throttle_rate))
        else:
            assert(self.throttle_rate == -1)


        num_dests = len(self.destination_links)
        if not (num_dests == 1 or (self.id == 0 and num_dests ==0 )):
            print("{0} has an issue".format(self.id))
            assert(1==2)


        if self.is_filter and self.bucket:
            # print("\n\n about to bucket")
            (legal_pass, legal_dropped, illegal_pass, illegal_dropped) = self.bucket.bucket_flow(self.legal_traffic, self.illegal_traffic, self.throttle_rate)
        else:
            if self.throttle_rate == -1:
                # if not set assume it's 0
                throttle_rate = 0
            else:
                throttle_rate = self.throttle_rate
            legal_dropped = self.legal_traffic * throttle_rate   
            legal_pass = self.legal_traffic - legal_dropped
            assert(abs(legal_pass + legal_dropped - self.legal_traffic) < EPSILON)

            illegal_dropped = self.illegal_traffic * throttle_rate
            illegal_pass = self.illegal_traffic - illegal_dropped
            assert(abs(illegal_pass + illegal_dropped - self.illegal_traffic) < EPSILON)

        # update all other switches with new traffic values

        # self.recorded_pass += (legal_pass + illegal_pass)
        # self.recorded_drop += (legal_dropped + illegal_dropped)

        for dest in self.destination_links:
            dest.destination_switch.new_legal += (legal_pass)
            dest.destination_switch.new_dropped_legal += ((legal_dropped + self.dropped_legal))

            dest.destination_switch.new_illegal += (illegal_pass)
            dest.destination_switch.new_dropped_illegal += ((illegal_dropped+ self.dropped_illegal))
            
        self.iterations_since_throttle += 1
    
    def updateSwitch(self,step):
        # update the traffic values
        self.legal_traffic = self.new_legal
        self.illegal_traffic = self.new_illegal
        self.dropped_legal = self.new_dropped_legal
        self.dropped_illegal = self.new_dropped_illegal

        # register switches interested in
        
        time_index = step%self.memory # the index of where to store the packet
        

        self.legal_window_estimate -= self.legal_segment[time_index]
        self.legal_window_estimate += self.legal_traffic
        self.illegal_window_estimate -= self.illegal_segment[time_index]
        self.illegal_window_estimate += self.illegal_traffic

        # dealing with floatign point errors.
        self.legal_window_estimate = max(0, self.legal_window_estimate)
        self.illegal_window_estimate = max(0, self.illegal_window_estimate)

        self.legal_segment[time_index] = self.legal_traffic
        self.illegal_segment[time_index] = self.illegal_traffic
        self.dropped_legal_segment[time_index] = self.dropped_legal
        self.dropped_illegal_segment[time_index] = self.dropped_illegal
        



        # reset new traffic values
        self.new_legal = 0
        self.new_illegal = 0
        self.new_dropped_legal = 0
        self.new_dropped_illegal = 0


        # reset the cache

        self.legal_dropped_window_cache = None
        self.illegal_dropped_window_cache = None
    def setThrottle(self, throttle_rate, is_new_def_action):
        # print(self.next_throttle)
        # print("next one is {0} at delay {1} move {2}".format(self.next_throttle, self.delay, self.iterations_since_throttle))
        if not (self.is_filter and (self.next_throttle == None or throttle_rate==self.next_throttle)):
            print(self.is_filter)
            print(self.next_throttle)
            print(throttle_rate)
            print(self.delay)
            print(self.throttle_rate)
            assert(1==2)
        if not is_new_def_action: #or throttle_rate==self.throttle_rate:
            # if it's the same don't do anything
            #self.next_throttle = None
            return
        else:
            self.next_throttle = throttle_rate
            self.iterations_since_throttle = 0 # we keep track of number iterations. This is for the delay of throttle


    def reset(self):
        self.legal_traffic = 0
        self.dropped_legal = 0
        self.illegal_traffic = 0
        self.dropped_illegal = 0
        self.new_legal = 0
        self.new_dropped_legal = 0
        self.new_illegal = 0
        self.new_dropped_illegal = 0
        self.throttle_rate = -1 # represents not set
        self.next_throttle = None
        self.iterations_since_throttle = 0
        #self.past_windows = [0]*20 obsolete

        # We keep track of the traffic that arrives at the switch over each step
        for i in range(len(self.legal_segment)):

            self.legal_segment[i] = 0  # over the last window, how much legal traffic has passed
            self.illegal_segment[i] = 0  # over the last window, how much illegal traffic has passed
            self.dropped_legal_segment[i] = 0 # how much legal traffic have we dropped over the last window
            self.dropped_illegal_segment[i] = 0  # over last window, how much illegal traffic has passed


        self.legal_dropped_window_cache = None
        self.illegal_dropped_window_cache = None
        if self.bucket:
            self.bucket.reset()


        #self.load_window_estimate = 0 # we use this for an estimate of the load at any time

        self.illegal_window_estimate = 0 # keep track
        self.legal_window_estimate = 0



    def printSwitch(self):
       print("switch_id {0} | load {1} | window {2}".format(self.id, self.legal_traffic + self.illegal_traffic, self.getWindow()))

    def get_illegal_window(self):
        return self.illegal_window_estimate

    def get_legal_window(self):
        return self.legal_window_estimate    

    def get_legal_dropped_window(self):
        if self.legal_dropped_window_cache != None:
            return self.legal_dropped_window_cache
        self.legal_dropped_window_cache = 0
        for segment in self.dropped_legal_segment:
            self.legal_dropped_window_cache += segment

        return self.legal_dropped_window_cache

    def get_illegal_dropped_window(self):
        if self.illegal_dropped_window_cache != None:
            return self.illegal_dropped_window_cache
        self.illegal_dropped_window_cache = 0
        for segment in self.dropped_illegal_segment:
            self.illegal_dropped_window_cache += segment

        return self.illegal_dropped_window_cache

    def get_load(self):
        illegal_window = self.get_illegal_window()
        legal_window = self.get_legal_window()
        load = illegal_window + legal_window

        return(KbToMb(load))


    # def getPastWindow(self, num_windows, step_size):
    #     answer = []
    #     for i in range(0, num_windows*step_size):
    #         if i%step_size==0:
    #             answer[-1] = KbToMb(answer[-1]) # convert to mb
    #             answer.append(0)
    #         j = i+1 
    #         answer[-1] += (self.legal_window[-j] + self.illegal_window[-j])

    #     answer[-1] = KbToMb(answer[-1]) # convert to mb
    #     return answer


    def setRepresentation(self, allThrottlers):
        self.stateSwitches.append(self) #always include self
         
        currentNode = self
        if self.representation == stateRepresentationEnum.throttler:
            pass

        elif self.representation == stateRepresentationEnum.allThrottlers:
            self.stateSwitches = allThrottlers
            assert(1==2) # haven't done delay for this yet!


        elif self.representation == stateRepresentationEnum.up_to_server:
            for i in range(3):
                print(currentNode.id)
                if currentNode.id==0:
                    break
                currentNode = currentNode.destination_links[0].destination_switch
                self.stateSwitches.append(currentNode)
                self.delay += 1                


           
        elif self.representation == stateRepresentationEnum.only_server:
            while currentNode.id != 0:
                currentNode = currentNode.destination_links[0].destination_switch
                self.delay += 1
            self.stateSwitches = [currentNode]
        else:
            print(self.representation)
            assert(1==2)

    def get_state(self):
        # get the state for the agent associated with the throttler
        response = []
        for switch in self.stateSwitches:
            response.append(switch.get_load())
        return response

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

class network_full(object):
    # a network simulator where we try simulate the traffic moving through the system
    name = "Network_Full"

    def __init__(self, network_settings, host_class, defender_settings, adversaryMaster, load_attack_path = None, save_attack=False):
        self.network_settings = network_settings
        self.iterations_between_second = network_settings.iterations_between_second# ideally set at 200
        self.host_sources = np.empty_like(network_settings.host_sources)
        self.host_sources[:] = network_settings.host_sources
        self.servers = np.empty_like(network_settings.servers)
        self.servers[:] = network_settings.servers # list of the servers. Usually [0]
        self.filter_list = network_settings.filters
        self.N_state = network_settings.N_state
        self.N_switch = network_settings.N_switch # number of nodes?
        self.N_host = len(self.host_sources)
        self.action_per_throttler = network_settings.action_per_throttler # actions each host can take
        #self.reward_overload = reward_overload
        self.rate_legal_low = MbToKb(network_settings.rate_legal_low)  #/ self.iterations_between_second)
        self.rate_legal_high = MbToKb(network_settings.rate_legal_high)  #/ self.iterations_between_second)
        self.rate_attack_low = MbToKb(network_settings.rate_attack_low)  #/ self.iterations_between_second)
        self.rate_attack_high = MbToKb(network_settings.rate_attack_high)  #/ self.iterations_between_second)

        self.representationType = defender_settings.stateRepresentation
        self.legal_probability = network_settings.legal_probability # odds of host being an attacker
        self.upper_bound = MbToKb(network_settings.upper_boundary) # for one second
        self.upper_boundary_two = self.upper_bound * 2 # for 2 seconds
        self.hostClass = host_class
        self.topology = []

        # specific to new network
        self.switches = [] # list of all switches, first one shouuld be attatched to server
        self.links = []
        self.throttlers = []
        self.hosts = []
        self.attack_record = [] # list of all attack stats, used if we're saving the attack

        self.adversaryMaster = adversaryMaster
        self.is_sig_attack = network_settings.is_sig_attack

        # self.SaveAttackEnum = SaveAttackEnum

        self.save_attack = save_attack
        self.load_attack_path = load_attack_path
        self.hostClass.classReset()
        bucket_capacity = MbToKb(network_settings.bucket_capacity)
        self.initialise(defender_settings, bucket_capacity)
        #self.last_state = np.empty_like(self.get_state())

    def reset(self):
        if self.load_attack_path: # if we provide a file to oad from use it
            self.load_attacker()
        else:
            self.generate_attackers()
        if self.save_attack:# is self.SaveAttackEnum.save:
            self.record_attackers()
        #self.set_rate()
        self.legitimate_sent_ep = 0
        self.legitimate_served_ep = 0
        self.illegal_sent_ep = 0
        self.illegal_served_ep = 0
        self.rewards_per_step = [] # keep track of the rewards at every step
        self.server_failures = 0


        # reset the switches)
        for i in range(self.N_switch):
            self.switches[i].reset()
        self.cache_reward = None


    def get_link(self, v):
        with open(self.network_settings.topologyFile) as f:
            count = 0
            for line in f:
                line = line.strip('\n')
                count += 1
                # Note I swapped dest/source from Yi as makes more sense for traffic going toward router
                dest_nd_id = int(line.split('-')[0])
                source_nd_id = int(line.split('-')[1])

                self.topology[source_nd_id][dest_nd_id] = v
                self.topology[dest_nd_id][source_nd_id] = v

            return count

    def generate_attackers(self):
        # sets a random amount of attackers inbetween (but not inclusive) 0 and max
        # I think just replace this if you want to replicate attacks

        attackers = []
        assert self.N_host!=0 or self.N_host!=1 # to stop infinite loops
        #do not allow "none/all attacker"
        attackers.clear()
        for i in range(self.N_host):
            if np.random.rand() >= self.legal_probability:
                attackers.append(i)
        
        if len(attackers) == 0 or len(attackers) >= (self.N_host-1):
            # requirements not satisfied
            return self.generate_attackers()

        self.hostClass.classReset()
        for i in range(len(self.hosts)):
            if i in attackers:
                self.hosts[i].reset(is_attacker=True)
            else:
               self.hosts[i].reset(is_attacker=False) 

        if self.is_sig_attack:
            max_bandwidth = 0 # maximum bandwidth that can be generated per turn
            for i in attackers:
                max_bandwidth += self.hosts[i].traffic_rate
            if max_bandwidth < 1.2*self.upper_bound:
                return self.generate_attackers()
     
    def record_attackers(self):
        host_details = []
        for host in self.hosts:
            host_details.append(host.get_details())

        self.attack_record.append(host_details)


    def load_attacker(self):
        host_data = self.saved_attack.pop()
        #print(host_data)
        for i in range(len(host_data)):
            self.hosts[i].load_details(host_data[i])





    def simulate_traffic(self, defender_action, adversary_action, step, is_new_def_action):
        # our defender action
        self.set_drop_probability(defender_action, is_new_def_action)
        self.adversaryMaster.sendTraffic(adversary_action)
        self.cache_reward = None
        for switch in self.switches:
            # move the traffic one spot
            switch.sendTraffic()

        for switch in self.switches:
            switch.updateSwitch(step)


    def set_drop_probability(self, actions, is_new_def_action):

        if self.representationType == stateRepresentationEnum.only_server:
            # if its only server then the actions is actually meant to be a throttle rate

            for switch_id in self.filter_list:
                self.switches[switch_id].setThrottle(actions, is_new_def_action)
        else:
            assert(self.N_state == len(actions))
            for i in range(self.N_state):
                action = actions[i]
                drop_prob = action/ self.action_per_throttler # to turn into a percentage
                switch_id = self.filter_list[i]
                self.switches[switch_id].setThrottle(drop_prob, is_new_def_action)


    def initialise(self, defender_settings, bucket_capacity):
        for i in range(self.N_switch):
            l = []
            for j in range(self.N_switch):
                l.append(-1)
            self.topology.append(l)

        n_lk = self.get_link(1)
        
        for i in range(self.N_switch):
            is_filter = i in self.filter_list
            self.switches.append(Switch(i, is_filter, self.representationType, defender_settings, self.iterations_between_second, bucket_capacity))

        
        for i in range(0, self.N_switch-1):
            for j in range(i, self.N_switch):
                if self.topology[i][j] != -1:
                    l = link()
                    l.id = len(self.links)
                    l.destination_switch = self.switches[i]
                    self.links.append(l)

                    self.switches[i].source_links.append(l)
                    self.switches[j].destination_links.append(l)                                    

        # print("\n\n\nfinished initialising")
        # for switch in self.switches:
        #     print("switch {1} len = {0}".format(len(switch.destination_links), switch.id))

        for i in self.host_sources:
            host = self.hostClass(self.switches[i], self.rate_attack_low, self.rate_attack_high,
                self.rate_legal_low, self.rate_legal_high, self.adversaryMaster, self.iterations_between_second)
            self.hosts.append(host)
        # set the state of all switches
        for i in self.filter_list:
            self.throttlers.append(self.switches[i])

        for throttler in self.throttlers:
            throttler.setRepresentation(self.throttlers)


        if self.load_attack_path:
            self.load_attacker_file()

        self.reset()


    def get_reward(self, reward_mode):
        """
        Used for calculating the reward.
        Return packets at the server, legal packets sent, legal packets served and Us (per second)
        """
        """
        3 Possible rewards:
        1) With overload: Return -1 if server is over capacity
        2) Sliding Negative: Return up to -1, the % over the server capacity
        3) We use the same metric as for evaluation, albeit over a 2 second period instead of 1
        """


        if self.cache_reward != None:
            return self.cache_reward

        legitimate_arrived = self.switches[0].get_legal_window()
        illegal_arrived = self.switches[0].get_illegal_window()
        legitimate_sent = legitimate_arrived + self.switches[0].get_legal_dropped_window()
        
        server_load = legitimate_arrived + illegal_arrived


        if server_load > (self.upper_boundary_two + EPSILON):
            # the three methods diverge how to respond to negative

            if reward_mode == AGENT_REWARD_ENUM.overload:
                # The only difference between sliding and overload is what happens when it's negative
                self.cache_reward = -1
                return self.cache_reward

            elif reward_mode == AGENT_REWARD_ENUM.sliding_negative:
                self.cache_reward = clip(-1, 1, -1*((server_load / self.upper_boundary_two)-1))
                return self.cache_reward

            elif reward_mode == AGENT_REWARD_ENUM.packet_logic:
                (legimate_served, illegal_served) = calcBottleNeck(server_load, legitimate_arrived, illegal_arrived, self.upper_boundary_two)

            else:
                assert(1==2)
        else:
            # we assume all traffic arriving is severd by the server
            legimate_served = legitimate_arrived
        

        self.cache_reward = clip(-1, 1, legimate_served / legitimate_sent) 
        return self.cache_reward






    def getHostCapacity(self):
        # return the packet capacity for attacker and legal traffic
        legal_traffic = 0
        illegal_traffic = 0
        for host in self.hosts:
            if host.is_attacker:
                illegal_traffic+=host.traffic_rate
            else:
                legal_traffic += host.traffic_rate
        legal_traffic = KbToMb(legal_traffic)
        illegal_traffic = KbToMb(illegal_traffic)
        combined = legal_traffic+ illegal_traffic
        return (legal_traffic, illegal_traffic, combined)


    def updateEpisodeStatistics(self, second):
        # to avoid a tonne of calculations. We're going to calculate this every second
        # note second is the second that has just passed


        time_start = (second%2) * self.iterations_between_second
        time_end = time_start + self.iterations_between_second

        legal_arrived = sum(self.switches[0].legal_segment[time_start:time_end])
        illegal_arrived = sum(self.switches[0].illegal_segment[time_start:time_end])
        legal_dropped = sum(self.switches[0].dropped_legal_segment[time_start:time_end])
        illegal_dropped = sum(self.switches[0].dropped_illegal_segment[time_start:time_end])
        
        # here we assume Malialis' evaluation technique
        server_load = legal_arrived + illegal_arrived
        
        legal_sent = (legal_arrived + legal_dropped)
        illegal_sent = ((illegal_arrived + illegal_dropped))

        if server_load > self.upper_bound:
            if self.network_settings.functionPastCapacity == True:

                # print(server_load)
                
                (legal_served, illegal_served) = calcBottleNeck(server_load, legal_arrived, illegal_arrived, self.upper_bound)

                assert(abs(legal_served+illegal_served - self.upper_bound) < 0.1)
            else:
                legal_served = 0
                illegal_served = 0
        else:
            legal_served = legal_arrived
            illegal_served = illegal_arrived
        # else:
        #     print("{0} < {1}".format(server_load, self.upper_bound))
        #     print(len(self.switches[0].illegal_segment[time_start:time_end]))
        #     print(len(self.switches[0].illegal_segment))
        #     print(self.iterations_between_second)
        #     print(self.getHostCapacity())

        self.legitimate_served_ep += legal_served
        self.legitimate_sent_ep += legal_sent
        self.illegal_served_ep += illegal_served
        self.illegal_sent_ep += illegal_sent

        per_served = legal_served / legal_sent
        return (legal_served, legal_sent, per_served, illegal_served, illegal_sent)
        # make sure not to update anything on the switch itself



    def getEpisodeStatisitcs(self):
        # returns % of packets served in an episode
        # meant to be used at end of an epsisode
        
        if self.legitimate_sent_ep == 0:
            legal_per = 0
            assert(1==2) # should never have sent 0
        else:
            legal_per = self.legitimate_served_ep / self.legitimate_sent_ep
        
        legit_serve_ep = KbToMb(self.legitimate_served_ep)
        legit_sent_ep = KbToMb(self.legitimate_sent_ep)
        illegal_served_ep = KbToMb(self.illegal_served_ep)
        illegal_sent_ep =  KbToMb(self.illegal_sent_ep)
        return (legit_serve_ep, legit_sent_ep, legal_per, illegal_served_ep, illegal_sent_ep)


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

    def printHostInformation(self):
        # for debugging
        attackers = []
        capacities = []
        attackCap = 0
        legCap = 0
        for host in self.hosts:
            attackers.append(host.is_attacker)
            tf = KbToMb(host.traffic_rate)
            capacities.append(tf)

            if host.is_attacker:
                attackCap += tf
            else:
                legCap += tf
        print(attackers)
        print(capacities)
        print("attack {0} legal {1}".format(attackCap, legCap))




def traverse(origin, targets, targetDic):
    # Starting at origin, travel along the network until we get a target
    # then update our dictionary to keep record of what is connected to what
    currentPosition = origin # a node of the network

    while (not currentPosition in targets):
        currentPosition = currentPosition.destination_links[0].destination_switch
        # should break if doesnt exist
    if not currentPosition in targetDic:
        targetDic[currentPosition] = []
    if not origin in targetDic[currentPosition]:
        targetDic[currentPosition].append(origin)

    
