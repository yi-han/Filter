import numpy as np
import random
"""
1) Shouldn't be keeping a counter, use the one provided by experiment
2) update to be handle variable

"""

class Host():
    # ideally you want to merge host with switch somewhat

    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, appendToSwitch=True):

        if appendToSwitch:
            destination_switch.attatched_hosts.append(self)
        
        self.destination_switch = destination_switch
        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high
        self.max_epLength = max_epLength
        self.reset(False) # initates all values

        assert(adversarialMaster == None)
    @staticmethod
    def classReset():
        return


    def reset(self, is_attacker, traffic_rate):
        self.is_attacker = is_attacker
        self.traffic_rate = traffic_rate

    def sendTraffic(self, time_step, send_rate):
        if self.is_attacker:
            self.destination_switch.new_illegal += send_rate
        else:
            self.destination_switch.new_legal += send_rate

    # def setRate(self, host_object):
    #     # manual alternative to resetting a host
    #     self.is_attacker = host_object.is_attacker
    #     self.traffic_rate = host_object.traffic_rate        

    def print_host(self):
        print("destination {0}".format(self.destination_switch.id))

    def getName():
        return "Generic-Host"


    def get_details(self):
        return (self.is_attacker, self.traffic_rate)

    def load_details(self, details):
        (is_attacker, traffic_rate) = details
        self.is_attacker = is_attacker
        self.traffic_rate = traffic_rate
class DriftAttack(Host):
    # pretty much like a constant attack except a small amount of the traffic will be considred legitimate traffic
    # as this is experimental we'll assume 5% of all traffic is set as legit


    def reset(self, is_attacker):

        if is_attacker:
            self.traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
        super().reset(is_attacker, traffic_rate)

    def sendTraffic(self, time_step):
        if self.is_attacker:
            self.destination_switch.new_illegal += self.traffic_rate*0.95
            self.destination_switch.new_legal += self.traffic_rate*0.05
        else:
            self.destination_switch.new_legal += self.traffic_rate
    
    def getName():
        return "Drift-Attack"


class ConstantAttack(Host):


    def reset(self, is_attacker):

        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)
        super().reset(is_attacker, traffic_rate)

    def sendTraffic(self, time_step):
        super().sendTraffic(time_step, self.traffic_rate)
    
    def getName():
        return "ConstantAttack"

class Pulse(Host):
    # pulse attack that changes every 2 seconds
    def __init__(self, time_flip, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster = None, appendToSwitch = True):

        self.time_flip = time_flip
        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, appendToSwitch)

    def sendTraffic(self, time_step):
        time_reduced = time_step % (2*self.time_flip) #split episode into two periods
        if time_reduced<=self.time_flip or not self.is_attacker:
            super().sendTraffic(time_step, self.traffic_rate)

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
        max_epLength, adversarialMaster = None, appendToSwitch = True):
        super().__init__(2, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, appendToSwitch)

    def getName():
        return "PulseShort"

class MediumPulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster = None, appendToSwitch = True):
        super().__init__(4, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, appendToSwitch)

    def getName():
        return "PulseMedium"


class LargePulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster = None, appendToSwitch = True):
        super().__init__(10, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster, appendToSwitch)
    def getName():
        return "PulseLarge"

class GradualIncrease(Host):

    def sendTraffic(self, time_step):
        if not self.is_attacker:
            super().sendTraffic(time_step, self.traffic_rate)
        percentageAttack = time_step/self.max_epLength
        assert(percentageAttack<=1)
        rate_traffic = self.init_traffic + (self.traffic_rate - self.init_traffic)*percentageAttack

        super().sendTraffic(time_step, rate_traffic)

    def getName():
        return "GradualIncrease"

    def reset(self, is_attacker):

        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
            # start the attack somewhat below the minimum attack but higher than the legal traffic
            self.init_traffic = self.rate_legal_high + np.random.rand()*(self.rate_attack_low - self.rate_legal_high)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)

        super().reset(is_attacker, traffic_rate)

class CoordinatedRandomNotGradual(Host):
    """
    everything but gradual attacks. Note all hosts work together (not a multivector attack)

    Things to be careful of:
    1) In the init of Host we attach our object to the switch. Quite likely that the switch might call us via switch
    so we can't be creating mulitple objects connected to switch. Best practice is to create a dummy switch for the fakes
    """
    possibleClasses = [ShortPulse, MediumPulse, LargePulse, ConstantAttack]
    assignedClass = None # this is iteratively updated based on the type of attack we're doing
    @staticmethod
    def classReset():
        CoordinatedRandomNotGradual.assignedClass = random.choice(CoordinatedRandomNotGradual.possibleClasses)


    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster = None, appendToSwitch = False):
        assert(appendToSwitch==False)
        # create a bunch of alterantive hosts that we can switch between
        self.active_host = None # the host that we are
        self.all_hosts = {}
        for hostClass in CoordinatedRandomNotGradual.possibleClasses:
            # the appendToSwitch=False is SUPER important
            self.all_hosts[hostClass] = (hostClass(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
                max_epLength, adversarialMaster, appendToSwitch))

        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength)



    def getName():
        return "RandomNotGradual"


    def reset(self, is_attacker):
        # create a temporary host of the assigned class
        self.active_host = CoordinatedRandomNotGradual.assignedClass
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



class adversarialRandom(object):
    """
    This is the host wrapper that pretends to be a set of hosts but in reality connects with 
    the adversarial Random Agent. We refer to it as random as we randomally assign the attack values
    It has many leaves, each which the network believes to be a host
    """


class adversarialLeaf(object):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength, adversarialMaster = None, appendToSwitch = True):

        assert(adversarialMaster != None)
        self.destination_switch = destination_switch

        if appendToSwitch:
            destination_switch.attatched_hosts.append(self)

        self.is_attacker = False # initiate as False

        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high

        self.adversarialMaster = adversarialMaster
        self.adversarialMaster.assignLeaf(self)


    def getName():
        return "AdversarialRandomMaster"

    def reset(self, is_attacker):
        if is_attacker:
            self.traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            self.traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)

    def setAgent(self, assignedAgent):
        # Adversarial Master will assign an agent this leaf belongs to
        self.agent = assignedAgent
    
    def classReset():
        return






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
