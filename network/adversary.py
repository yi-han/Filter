import numpy as np

class ConstantAttack():

    def __init__(self, N_host, attackers, rate_attack_low, rate_attack_high, rate_legal_low, rate_legal_high):
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

