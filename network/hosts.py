import numpy as np
import random
"""
1) Shouldn't be keeping a counter, use the one provided by experiment
2) update to be handle variable

"""




class Host():
    # ideally you want to merge host with switch somewhat

    def isAttackActive(self, time_step):
        return (self.first_attack <= time_step and time_step <= self.last_attack)

    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action,  appendToSwitch = True ):

        if appendToSwitch:
            destination_switch.attatched_hosts.append(self)
        self.destination_switch = destination_switch
        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high
        self.max_epLength = max_epLength
        self.iterations_per_action = iterations_per_action

        self.reset(False) # initates all values
        # unless we loading the attack, we constantly attack
        self.first_attack = 0
        self.last_attack = max_epLength
        assert(adversarialMaster == None)
    @staticmethod
    def classReset():
        return


    def reset(self, is_attacker, traffic_rate):
        self.is_attacker = is_attacker
        self.traffic_rate = traffic_rate
        self.traffic_per_iteration = self.traffic_rate/self.iterations_per_action

    def sendTraffic(self, time_step, packet_size):
        if self.is_attacker:
            if self.isAttackActive(time_step):
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
        self.first_attack = 5 # manually set
        self.last_attack = 55 # manually set


# class DriftAttack(Host):
#     # pretty much like a constant attack except a small amount of the traffic will be considred legitimate traffic
#     # as this is experimental we'll assume 5% of all traffic is set as legit


#     def reset(self, is_attacker):

#         if is_attacker:
#             self.traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
#         else:
#             self.traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
#         super().reset(is_attacker, self.traffic_rate)

#     def sendTraffic(self, time_step):
#         # set the drift initially to 20% illegal -> legal, 5% legal to illegal
#         if self.is_attacker:
#             self.destination_switch.new_illegal += self.traffic_rate*0.8
#             self.destination_switch.new_legal += self.traffic_rate*0.2
#         else:
#             self.destination_switch.new_legal += self.traffic_rate * 0.95
#             self.destination_switch.new_illegal += self.traffic_rate * 0.05
    
#     def getName():
#         return "Drift-Attack"


class ConstantAttack(Host):


    def reset(self, is_attacker):
        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
        super().reset(is_attacker, traffic_rate)

    def sendTraffic(self, time_step):
        super().sendTraffic(time_step, self.traffic_per_iteration)
    
    def getName():
        return "ConstantAttack"

class Pulse(Host):
    # pulse attack that changes every 2 seconds
    def __init__(self, time_flip, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch = True):

        self.time_flip = time_flip
        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch)

    def sendTraffic(self, time_step):
        time_reduced = time_step % (2*self.time_flip) #split episode into two periods

        if time_reduced<self.time_flip or not self.is_attacker:
            super().sendTraffic(time_step, self.traffic_per_iteration)

    def reset(self, is_attacker):
        # not sure if for pulse go all max or have different capacity
        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)

        super().reset(is_attacker, traffic_rate)

    def getName():
        return "PulseGeneric"

class ShortPulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch = True):
        super().__init__(1, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch)

    def getName():
        return "PulseShort"

class MediumPulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch = True):
        super().__init__(2, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch)

    def getName():
        return "PulseMedium"


class LargePulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch = True):
        super().__init__(5, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch)
    def getName():
        return "PulseLarge"

class GradualIncrease(Host):
    
    def sendTraffic(self, time_step):
        if not self.is_attacker:
            super().sendTraffic(time_step, self.traffic_per_iteration)
        else:
            percentageAttack = min(2*time_step/self.max_epLength,1)
            assert(percentageAttack<=1)
            #rate_traffic = self.init_traffic + (self.traffic_rate - self.init_traffic)*percentageAttack
            rate_traffic = self.traffic_per_iteration * percentageAttack
            super().sendTraffic(time_step, rate_traffic)

    def getName():
        return "GradualIncrease"

    def reset(self, is_attacker):

        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
            # start the attack somewhat below the minimum attack but higher than the legal traffic
            #self.init_traffic = self.rate_legal_high + np.random.rand()*(self.rate_attack_low - self.rate_legal_high)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
            #self.init_traffic = 0
        super().reset(is_attacker, traffic_rate)




class CoordinatedRandom(Host):
    """

    Things to be careful of:
    1) In the init of Host we attach our object to the switch. Quite likely that the switch might call us via switch
    so we can't be creating mulitple objects connected to switch. Best practice is to create a dummy switch for the fakes
    """
    possibleClasses = [ShortPulse, MediumPulse, LargePulse, ConstantAttack, GradualIncrease]
    assignedClass = None # this is iteratively updated based on the type of attack we're doing
    @staticmethod
    def classReset():
        CoordinatedRandom.assignedClass = random.choice(CoordinatedRandom.possibleClasses)


    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch = False):
        assert(appendToSwitch==False)
        # create a bunch of alterantive hosts that we can switch between
        self.active_host = None # the host that we are
        self.all_hosts = {}


        for hostClass in CoordinatedRandom.possibleClasses:
            # the appendToSwitch=False is SUPER important
            self.all_hosts[hostClass] = (hostClass(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
                max_epLength, adversarialMaster, iterations_per_action, appendToSwitch))


        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch)


    def getName():
        return "RandomAttack"


    def reset(self, is_attacker):
        # create a temporary host of the assigned class
        self.active_host = CoordinatedRandom.assignedClass
        #print("setting host as {0}".format(self.active_host))
        self.all_hosts[self.active_host].reset(is_attacker)


    def sendTraffic(self, time_step):
        self.all_hosts[self.active_host].sendTraffic(time_step)


    def get_details(self):

        (is_attacker, traffic_rate) = self.all_hosts[self.active_host].get_details()
        return (is_attacker, traffic_rate, self.active_host)

    def load_details(self, details):
        (is_attacker, traffic_rate, active_host) = details
        self.active_host = active_host
        self.active_host.load_details((is_attacker, traffic_rate))






class adversarialLeaf(Host):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, iterations_per_action, appendToSwitch=True):
        
        # self.destination_switch = destination_switch

        # if appendToSwitch:
        #     destination_switch.attatched_hosts.append(self)

        # self.is_attacker = False # initiate as False

        # self.rate_attack_low = rate_attack_low
        # self.rate_attack_high = rate_attack_high
        # self.rate_legal_low = rate_legal_low
        # self.rate_legal_high = rate_legal_high
        # self.iterations_per_action = iterations_per_action
        # if max_epLength != -1: 
        #     assert(adversarialMaster != None)
        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, None, iterations_per_action, appendToSwitch)
        
        if max_epLength != -1:
            self.adversarialMaster = adversarialMaster
            self.adversarialMaster.addLeaf(self)
        else:
            self.adversarialMaster = None


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
        packet_size = (self.traffic_per_iteration)*percent_emit
        if self.is_attacker:
            self.destination_switch.new_illegal += packet_size
        else:
            self.destination_switch.new_legal += self.traffic_per_iteration        

"""

class Pulse():
    # aim to have a super class for pulses
    def __init__(self, N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, swap_at):
        self.pulse_host = []
        self.standard_host = []
        self.max_epLength = max_epLength
        
        self.swap_at=swap_at
        self.counter = 0
        self.pulse_on = False
        for i in range(N_host):
            if i in attackers:
                self.pulse_host.append(rate_attack_low + np.random.rand()*(rate_attack_high - rate_attack_low))
                self.standard_host.append(0)
            else:
                self.pulse_host.append(rate_legal_low + np.random.rand()*(rate_legal_high - rate_legal_low))
                self.standard_host.append(rate_legal_low + np.random.rand()*(rate_legal_high - rate_legal_low))
        self.host_rate = self.standard_host

    def takeStep(self):
        self.counter +=1

        if self.counter % self.swap_at == 0:
            if self.pulse_on:
                self.pulse_on = False
                self.host_rate = self.standard_host
            else:
                self.pulse_on = True
                self.host_rate = self.pulse_host



    def getHostRate(self):
        return self.host_rate


class PulseQuick(Pulse):

    def __init__(self, N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):
        super().__init__(N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, 2)


class PulseMedium(Pulse):
    def __init__(self, N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):
        super().__init__(N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, 4)


"""
