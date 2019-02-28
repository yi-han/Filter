#import requests
#import json
import numpy as np
import math
#import copy
import pickle
from mapsAndSettings import stateRepresentationEnum, advesaryTypeEnum
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





class Bucket():
    # for buckets associated to a switch

    def __init__(self, iterations_between_action, bucket_capacity ):
        self.iterations_between_action = iterations_between_action
        self.bucket_capacity = bucket_capacity
        self.reset()
    def reset(self):
        self.bucket_list = [] # to ensure FIFO
        self.bucket_load = 0

    def updateBucketLoad(self, traffic_changed, is_incoming):
        if is_incoming:
            assert(traffic_changed>0)
            self.bucket_load += traffic_changed
        else:
            assert(traffic_changed > 0)
            self.bucket_load -= traffic_changed
            self.bucket_load = max(0, self.bucket_load)
    def bucket_flow(self, legal_traffic_in, illegal_traffic_in, rs_per_action):
        """
        Bucket logic
        Current idea:
        All data must add to the bucket first. Only then can we take it out
        Rationale: We're breaking it down to 10ms steps anyway. The memory would include the ram
        
        Initial idea:
        Case 1: Bucket load is less than rs

        Case 2:
        Bucket + traffic in exceeds bucket_load

        Case 3 (easy):
        rs < Bucket < Bucket + rs < bucket_load


        First calculate out from the bucket.
        Then calculate what to do with new traffic
        """

        if rs_per_action == None:
            # No throttle set
            rs_per_iteration = INF
        else:
            rs_per_iteration = roundNumber(MbToKb(rs_per_action/self.iterations_between_action))
        # adding data to bucket
        
        #print("legal {0} illegal {1} rs {2}".format(legal_traffic_in, illegal_traffic_in, rs_per_iteration))
        legal_traffic_in = roundNumber(legal_traffic_in)
        illegal_traffic_in = roundNumber(illegal_traffic_in)
        remaining_capacity = self.bucket_capacity - self.bucket_load
        # print("load {0} total capacity {1} remaining {2}".format(self.bucket_load, self.bucket_capacity, remaining_capacity))
        # print("capacity is {1} whilst incoming load is {0}".format((illegal_traffic_in+legal_traffic_in),remaining_capacity))
        if remaining_capacity < DELTA:
            # already full? shouldn't ever be case
            assert(1==2)
            (legal_dropped, illegal_dropped) = (legal_traffic_in, illegal_traffic_in)
        else:
            (legal_added, legal_dropped, illegal_added, illegal_dropped) = self.add_to_capacity(legal_traffic_in, illegal_traffic_in, remaining_capacity)
            # print((legal_added, legal_dropped, illegal_added, illegal_dropped))
            #assert(abs(legal_added+legal_dropped-legal_traffic_in)<DELTA)
            #assert(abs(illegal_added+illegal_dropped-illegal_traffic_in)<DELTA)


            self.add_bucket(legal_added, illegal_added)
             

        # empty bucket
        legal_out, illegal_out = self.empty_bucket(rs_per_iteration)
        # print("illegal into bucket {0} and illegal out {1} with rate {2}".format(illegal_added, illegal_out, rs_per_iteration))

        return (legal_out, legal_dropped, illegal_out, illegal_dropped)


    def add_bucket(self, legal_in, illegal_in, at_front=False):
        # add to bucket
        legal_in = max(legal_in, 0)
        illegal_in = max(illegal_in, 0)
        if (legal_in + illegal_in) < DELTA:
            return
        if at_front:
            self.bucket_list.insert(0, (legal_in, illegal_in))
        else:
            self.bucket_list.append((legal_in, illegal_in))
        self.updateBucketLoad((legal_in + illegal_in), True)
        if self.bucket_load-self.bucket_capacity>DELTA:
            print("we're over by {0}".format(self.bucket_load-self.bucket_capacity))
            assert(1==2)
        assert(self.bucket_load-self.bucket_capacity < DELTA)

    def empty_bucket(self, current_rs):
        # empty bucket to amount of rs or until empty
        
        assert(self.bucket_load - self.bucket_capacity < DELTA)
        emptied = 0
        legal_out = 0
        illegal_out = 0
        remaining_rs = current_rs
        (legal_added, legal_stopped, illegal_added, illegal_stopped) = (0, 0, 0, 0) # this is for santify checking assetts
        while(self.bucket_list and remaining_rs>DELTA):
            assert(legal_stopped<DELTA and illegal_stopped < DELTA)

            (f_legal, f_illegal) = self.bucket_list.pop(0)
            (legal_added, legal_stopped, illegal_added, illegal_stopped) = self.add_to_capacity(f_legal, f_illegal, remaining_rs)
            remaining_rs -= (f_legal + f_illegal) # note this will go negative once we hit our limit
            legal_out += legal_added
            illegal_out += illegal_added
            self.updateBucketLoad((f_legal + f_illegal), False)
        #if((legal_stopped + illegal_stopped) > DELTA):
            # put back to bucket any that didn't get through
            # print("put back in ")
            # print("out {0} {1} | stopped {2} {3} | remaining_capacity {4} | f {5} {6}".format(legal_added, illegal_added, legal_stopped, illegal_stopped, (self.bucket_capacity - self.bucket_load), f_legal, f_illegal))
            # print("remaining once added {0} | load {1}".format((self.bucket_capacity - self.bucket_load- (legal_stopped + illegal_stopped)), self.bucket_load))
        # add bucket will ensure we aren't adding stupid stuff
        self.add_bucket(legal_stopped, illegal_stopped, at_front=True)
        return (legal_out, illegal_out)

    def add_to_capacity(self, legal_in, illegal_in, capacity):
        # print("in {0} {1} capacity {2}".format(legal_in, illegal_in, capacity))

        traffic_in = legal_in + illegal_in

        assert(capacity>0 and traffic_in >= 0)

        if(traffic_in<DELTA):
            return (0, 0, 0, 0)

        percentage_through = min((capacity/traffic_in),1)
        # print("percentage was {0}".format(percentage_through))
        # print("leg {0} ill {1} cap {2}".format(legal_in, illegal_in, capacity))

        legal_added = round_half_down(percentage_through*legal_in)
        illegal_added = round_half_down(percentage_through*illegal_in)

        legal_stopped = round_half_down(legal_in - legal_added)
        illegal_stopped = round_half_down(illegal_in - illegal_added)

        if((legal_added + illegal_added-capacity)>DELTA):
            print("legal_added {0} illegal_added {1} capacity {2} combined {3}".format(legal_added, illegal_added, capacity, legal_added+illegal_added))
            assert(1==2)
        return (legal_added, legal_stopped, illegal_added, illegal_stopped)


class Switch():
    def __init__(self, switch_id, is_filter, representation, defender_settings, iterations_between_action, bucket_capacity):
        self.id = switch_id # id
        self.source_links = [] # places sending traffic to switch
        self.destination_links = [] # where traffic is getting sent
        self.attatched_hosts = [] # used for network_quick, quick access for hosts attatched to this 
        self.throttle_rate = None # the throttling rate for the specific switch
        
        self.legal_window = 0 # over the last window, how much legal traffic has passed
        self.illegal_window = 0 # over the last window, how much illegal traffic has passed
        self.dropped_legal_window = 0 # how much legal traffic have we dropped over the last window
        self.dropped_illegal_window = 0 # over last window, how much illegal traffic has passed

        self.legal_traffic = 0
        self.dropped_legal = 0
        self.illegal_traffic = 0
        self.dropped_illegal = 0

        self.new_legal = 0
        self.new_dropped_legal = 0
        self.new_illegal = 0
        self.new_dropped_illegal = 0

        self.stateSwitches = [] # list of objects we use for state. If just self it shows only load at self

        self.associated_throttlers = [] ### only used by network_quick
        self.representation = representation

        self.is_filter = is_filter

        if defender_settings.has_bucket and is_filter:
            # initiate a bucket
            self.bucket = Bucket(iterations_between_action, bucket_capacity)
        else:
            self.bucket = None
        self.reset()

        self.delay = 0 # the delay for implementing a throttle based on maximum communication
    def sendTraffic(self):
        # an initial part of passing traffic along


        if self.is_filter:
            if self.iterations_since_throttle == self.delay:
                self.throttle_rate = self.next_throttle
            # print("delay {0} throttle {1}".format(self.delay - self.iterations_since_throttle, self.throttle_rate))
        else:
            assert(self.throttle_rate == None)


        num_dests = len(self.destination_links)
        assert(num_dests == 1 or (self.id == 0 and num_dests ==0))

        if self.is_filter and self.bucket:
            # print("\n\n about to bucket")
            (legal_pass, legal_dropped, illegal_pass, illegal_dropped) = self.bucket.bucket_flow(self.legal_traffic, self.illegal_traffic, self.throttle_rate)
        else:
            if self.throttle_rate == None:
                # if not set assume it's 0
                throttle_rate = 0
            else:
                throttle_rate = self.throttle_rate
            legal_dropped = roundNumber(self.legal_traffic * throttle_rate)      
            legal_pass = self.legal_traffic - legal_dropped
            assert(abs(legal_pass + legal_dropped - self.legal_traffic) < DELTA)

            illegal_dropped = roundNumber(self.illegal_traffic * throttle_rate)
            illegal_pass = self.illegal_traffic - illegal_dropped
            #assert(abs(illegal_pass + illegal_dropped - self.illegal_traffic) < DELTA)

        # update all other switches with new traffic values

        self.recorded_pass += (legal_pass + illegal_pass)
        self.recorded_drop += (legal_dropped + illegal_dropped)

        for dest in self.destination_links:
            dest.destination_switch.new_legal += (legal_pass/num_dests)
            dest.destination_switch.new_dropped_legal += ((legal_dropped + self.dropped_legal)/num_dests)

            dest.destination_switch.new_illegal += (illegal_pass/num_dests)
            dest.destination_switch.new_dropped_illegal += ((illegal_dropped+ self.dropped_illegal)/num_dests)
            
        self.iterations_since_throttle += 1
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

        self.recorded_pass = 0 # we use this to calculate the average throttle in each step
        self.recorded_drop = 0

    def getWindow(self):
        return KbToMb(self.legal_window + self.illegal_window)

    def getImmediateState(self):
        return self.legal_traffic + self.illegal_traffic

    def setThrottle(self, throttle_rate):

        assert(self.is_filter)
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
        self.resetWindow()
        self.throttle_rate = None # represents not set
        self.iterations_since_throttle = 0
        if self.bucket:
            self.bucket.reset()




    def printSwitch(self):
       print("switch_id {0} | load {1} | window {2}".format(self.id, self.legal_traffic + self.illegal_traffic, self.getWindow()))

    def setRepresentation(self, allThrottlers):
        self.stateSwitches.append(self) #always include self
         
        currentNode = self
        if self.representation == stateRepresentationEnum.throttler:
            pass

        elif self.representation == stateRepresentationEnum.allThrottlers:
            self.stateSwitches = allThrottlers
            assert(1==2) # haven't done delay for this yet!
        elif self.representation == stateRepresentationEnum.leaderAndIntermediate:
            for i in range(2):
                currentNode = currentNode.destination_links[0].destination_switch
                assert currentNode.id!=0 #we shouldn't be getting server
                #print(currentNode.id)
                self.stateSwitches.append(currentNode)
                self.delay += 1

        elif self.representation == stateRepresentationEnum.server:
            for i in range(3):
                currentNode = currentNode.destination_links[0].destination_switch
                assert currentNode.id!=0 #we shouldn't be getting server
                #print(currentNode.id)
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
            response.append(switch.getWindow())
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

    # def __init__(self, N_switch, N_action, N_state, action_per_throttler, host_sources, servers, filter_list, reward_overload, 
    #           rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
    #           legal_probability, upper_boundary, hostClass, max_epLength, f_link, SaveAttackEnum,
    #           save_attack, load_attack_path):

    #self.ITERATIONSBETEENACTION = 200 # with 10 ms delay, and throttle agent every 2 seconds, we see 200 messages passed in between
    name = "Network_Full"

    def __init__(self, network_settings, reward_overload, host_class, max_epLength, representationType, defender_settings, adversaryMaster, load_attack_path = None, save_attack=False):
        
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
        self.rate_legal_low = MbToKb(network_settings.rate_legal_low)  #/ self.iterations_between_action)
        self.rate_legal_high = MbToKb(network_settings.rate_legal_high)  #/ self.iterations_between_action)
        self.rate_attack_low = MbToKb(network_settings.rate_attack_low)  #/ self.iterations_between_action)
        self.rate_attack_high = MbToKb(network_settings.rate_attack_high)  #/ self.iterations_between_action)

        self.representationType = representationType
        self.legal_probability = network_settings.legal_probability # odds of host being an attacker
        self.upper_boundary = MbToKb(network_settings.upper_boundary)
        self.hostClass = host_class
        self.topology = []
        self.max_epLength = max_epLength

        # specific to new network
        self.switches = [] # list of all switches, first one shouuld be attatched to server
        self.links = []
        self.throttlers = []
        self.hosts = []
        self.attack_record = [] # list of all attack stats, used if we're saving the attack

        self.adversaryMaster = adversaryMaster
        self.is_sig_attack = network_settings.is_sig_attack
        self.drift = network_settings.drift / 100
        # drift is the measure of inaccurecy of discretising legitimate from illegite traffic
        # represents the % of illegal traffic set as legal.

        # self.SaveAttackEnum = SaveAttackEnum

        self.save_attack = save_attack
        self.load_attack_path = load_attack_path
        self.hostClass.classReset()
        bucket_capacity = MbToKb(network_settings.bucket_capacity)
        self.initialise(network_settings.topologyFile, representationType, defender_settings, network_settings.iterations_between_action, bucket_capacity)
        self.last_state = np.empty_like(self.get_state())

    def reset(self):
        if self.load_attack_path: # if we provide a file to oad from use it
            self.load_attacker()
        else:
            self.generate_attackers()
        if self.save_attack:# is self.SaveAttackEnum.save:
            self.record_attackers()
        #self.set_rate()
        self.current_state = None
        self.legitimate_all = 0
        self.legitimate_served = 0
        self.rewards_per_step = [] # keep track of the rewards at every step
        self.server_failures = 0

        # reset the switches)
        for i in range(self.N_switch):
            self.switches[i].reset()



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
        
        if len(attackers) == 0 or len(attackers) == self.N_host:
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
            if max_bandwidth < self.upper_boundary:
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


    def get_state(self):
        # get the state for the agent associated with the throttler
        
        if self.current_state:
            # we're trying to cache the current state
            return self.current_state

        response = []
        for i in self.filter_list:
            response.append(self.switches[i].get_state())
        
        # error checking. Print out full state
        # full_state = []
        # for switch in self.switches:
        #     full_state.append(switch.getWindow())

        # print("given State")
        # print(response)
        # print("global State")
        # print(full_state)

        self.current_state = response
        return response

        
    def move_traffic(self, time_step, adv_action):
        # update the network
        if adv_action:
            assert( self.adversaryMaster!=None)

            self.adversaryMaster.sendTraffic(adv_action)
        else:
            for host in self.hosts:
                host.sendTraffic(time_step)

        for switch in self.switches:
            # ensure all traffic sent before we update
            #print(defender_agent)
            switch.sendTraffic()

        for switch in self.switches:
            # simulates adding new traffic to the hosts
            switch.updateSwitch()

    def set_drop_probability(self, action):

        if self.representationType == stateRepresentationEnum.only_server:
            # if its only server then the action is actually meant to be a throttle rate

            for switch_id in self.filter_list:
                self.switches[switch_id].setThrottle(action)
        else:
            for i in range(self.N_state):
                j = self.N_state - (i + 1) # start at one below host, end at 0
                divider = self.action_per_throttler**j

                switch_id = self.filter_list[i]
                drop_prob = int(action / divider)
                action = action - (drop_prob*divider)
                drop_prob /= self.action_per_throttler # to turn into a percentage
                self.switches[switch_id].setThrottle(drop_prob)

            assert(action==0) 

    def initialise(self, f_link, representationType, defender_settings, iterations_between_action, bucket_capacity):
        for i in range(self.N_switch):
            l = []
            for j in range(self.N_switch):
                l.append(-1)
            self.topology.append(l)

        n_lk = self.get_link(self.topology, f_link, 1)
        
        for i in range(self.N_switch):
            is_filter = i in self.filter_list
            self.switches.append(Switch(i, is_filter, representationType, defender_settings, iterations_between_action, bucket_capacity))

        
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
                self.rate_legal_low, self.rate_legal_high, self.max_epLength, self.adversaryMaster, self.iterations_between_action)
            self.hosts.append(host)
        # set the state of all switches
        for i in self.filter_list:
            self.throttlers.append(self.switches[i])

        for throttler in self.throttlers:
            throttler.setRepresentation(self.throttlers)


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

    def adjust_drift(self):
        #obsolete
        assert(1==2)
        # assume there is some drift, we want to return the stats with the associated drift

        # Drift rules:
        # Drift implies % illegal traffic categorised as legal traffic
        # also have 25% of that rate of legal traffic set as illegal traffic

        legitimate_rate = self.switches[0].legal_window
        legitimate_rate_all = legitimate_rate + self.switches[0].dropped_legal_window
        attacker_rate = self.switches[0].illegal_window
        attacker_rate_all = attacker_rate + self.switches[0].dropped_illegal_window

        illegal_to_legal = self.drift # illegal traffic misclassified as legal
        legal_to_illegal = 0.25*self.drift # legal traffic misclassified as illegal

        new_legit_rate = (1 - legal_to_illegal)* legitimate_rate + (illegal_to_legal * attacker_rate)
        new_attacker_rate = (1 - illegal_to_legal) * attacker_rate + (legal_to_illegal*legitimate_rate)
        new_legitimate_rate_all = (1 - legal_to_illegal)* legitimate_rate_all + (illegal_to_legal * attacker_rate_all)

        #print("{0} {1} {2} To {3} {4} {5}".format(legitimate_rate, legitimate_rate_all, attacker_rate,
        #        new_legit_rate, new_legitimate_rate_all, new_attacker_rate))

        return (new_legit_rate, new_legitimate_rate_all, new_attacker_rate)
    def calculate_reward(self):
        
        if self.cache_reward != None:
            return self.cache_reward

        # currently if we're 1.1 times over we receive a punishment of -0.1, seems rather low. Maybe -1.5?        
        reward = 0.0

        legitimate_rate = self.switches[0].legal_window
        legitimate_rate_all = legitimate_rate + self.switches[0].dropped_legal_window
        attacker_rate = self.switches[0].illegal_window
        #assert((legitimate_rate+attacker_rate)==self.switches[0].getWindow())

        if legitimate_rate + attacker_rate > self.upper_boundary:
            #used to set the reward to "reward_overload" in this case, but didn't work well
           
            # print("\n\n\n negative reward")
            # print(self.upper_boundary)
            if self.reward_overload:
                reward = self.reward_overload
            else:
                reward -= ((legitimate_rate + attacker_rate)/self.upper_boundary - 1.0)
            
            self.server_failures +=1

            # throttle the traffic at the server down to capacity
            # the negative is you're having to throttle at the server as opposed to at the enemy
            # I deactivated it as the results (apart from gradually increasing) all were closer without
            if False:
                traffic_level = legitimate_rate + attacker_rate
                overload_amount = traffic_level - self.upper_boundary
                overload_percent = overload_amount/traffic_level
                server_throttle_level = 1-overload_percent
                assert(abs(server_throttle_level * traffic_level - self.upper_boundary )< DELTA) 
                new_legit_rate = legitimate_rate * server_throttle_level
                #print("{0} vs {1}".format(new_legit_rate, legitimate_rate_all))
                self.legitimate_served += new_legit_rate

        else:
            # we dont do the drift until now because before now it didn't matter
            # print("\nprior")
            # print("{0} {1} {2} = {3}".format(legitimate_rate, legitimate_rate_all, attacker_rate, legitimate_rate/legitimate_rate_all))
            #legitimate_rate, legitimate_rate_all, attacker_rate = self.adjust_drift()
            # print("{0} {1} {2} = {3}".format(legitimate_rate, legitimate_rate_all, attacker_rate, legitimate_rate/legitimate_rate_all))

            if legitimate_rate_all != 0:
                reward += legitimate_rate/legitimate_rate_all
        
            self.legitimate_served += legitimate_rate
        
        self.legitimate_all += legitimate_rate_all

        reward = clip(-1, 1, reward)

        self.cache_reward = reward
        return reward

    def getPacketServedAtMoment(self):
        """
        Experimental statistic. 
        Calculate the load at the server. If it is above the capacity/steps report 0. 
        Otherwise the % of legitimate packets taht should have arrived.
        Do note there is an accumulative effect so this is very imprecise

        """
        legitimate_rate = self.switches[0].legal_window
        legitimate_sent = self.switches[0].legal_window + self.switches[0].dropped_legal_window
        attacker_rate = self.switches[0].illegal_window

        if legitimate_rate + attacker_rate > self.upper_boundary:
            return 0.0
        else:
            return MbToKb(legitimate_rate/legitimate_sent)


    def step(self, action, step_count, adv_action = None):
        # input the actions. Just sets drop probabilities at the moment
        # ideally i would move calculations here
        # adv action is action by adversary
        self.cache_reward = None 
        self.last_state = self.get_state()
        self.current_state = None # we need to reset the state to undo the cache
        for switch in self.switches:
            switch.resetWindow()
        
        self.set_drop_probability(action)
        

        # reset_throttle_count and record_average_throttle seek to determine what the true throttle percentage actually was
        for i in range(self.iterations_between_action): # each time delay is 10 ms, 10*200 = 2000 ms = 2 seconds
           self.move_traffic(step_count, adv_action)
           #self.rewards_per_step.append(self.calculate_reward())

        #self.record_average_throttle()

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

    # def record_average_throttle(self):
    #     for switch in self.switches:
    #         if (switch.recorded_drop + switch.recorded_pass) == 0:
    #             new_throttle = 0
    #         else:
    #             new_throttle = switch.recorded_drop / (switch.recorded_drop + switch.recorded_pass)
    #         switch.past_throttles.append(new_throttle*10) # convert to a whole number
    #         switch.past_throttles.pop(0)



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

    
