import numpy as np
import random
import network.utility as utility
"""
1) Shouldn't be keeping a counter, use the one provided by experiment
2) update to be handle variable

"""




class Host():
    # ideally you want to merge host with switch somewhat

    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        adversarialMaster, iterations_between_second,  appendToSwitch = True ):

        if appendToSwitch:
            destination_switch.attatched_hosts.append(self)
        self.destination_switch = destination_switch
        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high
        self.iterations_between_second = iterations_between_second

        self.reset(False) # initates all values
        # unless we loading the attack, we constantly attack

        assert(adversarialMaster == None)
    @staticmethod
    def classReset():
        return


    def reset(self, is_attacker, traffic_rate):
        self.is_attacker = is_attacker
        self.traffic_rate = traffic_rate
        self.traffic_per_iteration = self.traffic_rate/self.iterations_between_second

    def sendTraffic(self, packet_size):
        if self.is_attacker:
            self.destination_switch.new_illegal += packet_size
        if not self.is_attacker:
            self.destination_switch.new_legal += packet_size



    def print_host(self):
        print("destination {0}".format(self.destination_switch.id))

    def getName():
        return "Generic-Host"


    def get_details(self):
        return (self.is_attacker, self.traffic_rate)

    def load_details(self, details):
        # note this only happens if we're loading the attack. Therefore 
        # we start the attack at step 5 and stops at t=55
        (is_attacker, traffic_rate) = details
        Host.reset(self, is_attacker, traffic_rate)





class ConstantAttack(Host):


    def reset(self, is_attacker):
        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
        super().reset(is_attacker, traffic_rate)

    def sendTraffic(self):
        super().sendTraffic(self.traffic_per_iteration)
    
    def getName():
        return "ConstantAttack"



class adversarialLeaf(Host):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        adversarialMaster, iterations_between_second, appendToSwitch=True):
        
        # self.destination_switch = destination_switch

        # if appendToSwitch:
        #     destination_switch.attatched_hosts.append(self)

        # self.is_attacker = False # initiate as False

        # self.rate_attack_low = rate_attack_low
        # self.rate_attack_high = rate_attack_high
        # self.rate_legal_low = rate_legal_low
        # self.rate_legal_high = rate_legal_high
        # self.iterations_between_second = iterations_between_second
        # if max_epLength != -1: 
        #     assert(adversarialMaster != None)
        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        None, iterations_between_second, appendToSwitch)
        
        #if max_epLength != -1:
        self.adversarialMaster = adversarialMaster
        self.adversarialMaster.addLeaf(self)
        #else:
        #    self.adversarialMaster = None


    def getName():
        return "AdversarialRandomMaster"

    def reset(self, is_attacker):
        self.is_attacker = is_attacker
        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
        super().reset(is_attacker, traffic_rate)
    
    def setAgent(self, assignedAgent):
        # Adversarial Master will assign an agent this leaf belongs to
        self.agent = assignedAgent


    def sendTraffic(self, percent_emit):
        assert(percent_emit<=1)

        rate_traffic = self.traffic_per_iteration * percent_emit
        
        if self.is_attacker:
            super().sendTraffic(rate_traffic)
        else:
            super().sendTraffic(self.traffic_per_iteration)


