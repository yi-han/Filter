import numpy as np

class ConstantAttack():

    def __init__(self, N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high,
        max_epLength):
        self.host_rate = []
        
        for i in range(N_host):
            if i in attackers:
                self.host_rate.append(rate_attack_low + np.random.rand()*(rate_attack_high - rate_attack_low))
            else:
                self.host_rate.append(rate_legal_low + np.random.rand()*(rate_legal_high - rate_legal_low))


    def takeStep(self):
        pass

    def getHostRate(self):
        return self.host_rate


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



