import numpy as np
"""
1) Shouldn't be keeping a counter, use the one provided by experiment
2) update to be handle variable

"""

class Host():
    # ideally you want to merge host with switch somewhat

    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):

        self.destination_switch = destination_switch

        self.rate_attack_low = rate_attack_low
        self.rate_attack_high = rate_attack_high
        self.rate_legal_low = rate_legal_low
        self.rate_legal_high = rate_legal_high
        self.max_epLength = max_epLength
        self.reset(False) # initates all values

    def reset(self, is_attacker, traffic_rate):
        self.is_attacker = is_attacker
        self.traffic_rate = traffic_rate

    def sendTraffic(self, time_step, send_rate):
        if self.is_attacker:
            self.destination_switch.new_illegal += send_rate
        else:
            self.destination_switch.new_legal += send_rate


    def print_host(self):
        print("destination {0}".format(self.destination_switch.id))

    def getName():
        return "Generic-Host"

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
        return "Constant-Attack"

class Pulse(Host):
    # pulse attack that changes every 2 seconds
    def __init__(self, time_flip, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):

        self.time_flip = time_flip
        super().__init__(destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength)

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
        return "Pulse-Generic"

class ShortPulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):
        super().__init__(2, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength)

    def getName():
        return "Pulse-Short"

class MediumPulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):
        super().__init__(4, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength)

    def getName():
        return "Pulse-Medium"


class LargePulse(Pulse):
    def __init__(self, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):
        super().__init__(10, destination_switch, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength)
    def getName():
        return "Pulse-Large"

class GradualIncrease(Host):

    def sendTraffic(self, time_step):
        if not self.is_attacker:
            super().sendTraffic(time_step, self.traffic_rate)
        min_traffic = self.rate_attack_low
        percentageAttack = time_step/self.max_epLength
        rate_traffic = min_traffic + ((self.traffic_rate) - min_traffic)*percentageAttack

        super().sendTraffic(time_step, rate_traffic)

    def getName():
        return "Gradual-Increase"

    def reset(self, is_attacker):

        if is_attacker:
            traffic_rate = self.rate_attack_low + np.random.rand()*(self.rate_attack_high - self.rate_attack_low)
        else:
            traffic_rate = self.rate_legal_low + np.random.rand()*(self.rate_legal_high - self.rate_legal_low)

        super().reset(is_attacker, traffic_rate)


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
