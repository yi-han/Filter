"""
The baseline agent used in Mah used for comparative purposes

Really Im only creating this as a step to create MARL

Do I need to model in network delays for each throttler? 
Technically differnt throttlers can receive their mark at differnt times

TODO
1) Network delays?
2) Initial rate probably set wrong as the formula is for through rate per second but window is 2 seconds
    sort of fixed
3) What throttle rate do i simulate for smart adversary? 
"""

class AIMDagent():
    def __init__(self, network_settings, agent_settings):
        self.num_throttles = network_settings.N_state
        self.delta = agent_settings.delta # for rate increase
        self.beta = agent_settings.beta # for rate decrease
        self.epsilon = agent_settings.epsilon
        self.upper = network_settings.upper_boundary
        self.lower = network_settings.lower_boundary
        self.seconds_per_window = 2 ### UPDATE: probably shouldn't assume
        self.iterations_per_window = network_settings.iterations_between_action
    def __enter__(self):
        print("enter the AIMD")
        self.reset()

    def __exit__(self, type, value, tb):
        print("exit the AIMD")

    def reset(self):
        self.rs = -1
        self.pLast = -1        

    def predict(self, p, _):
        # treat this as set the rate
        # p is server load
        # we calculate the maximum amount of traffic we allow pass through in a 
        p = p[0][0]
        if p > self.upper:
            if self.rs < 0:
                self.rs  = (self.upper + self.lower)/self.num_throttles
            else:
                self.rs /= self.beta
            self.pLast = p
        elif p < self.lower:
            if abs(p - self.pLast) < self.epsilon:
                self.rs = -1
                self.pLast = -1
            else:
                self.pLast = p
                self.rs += self.delta
        return 0

    def update(self, _, _a, _b, _c, _d, _e = 0):
        return

    def actionReplay(self, _a, _b):
        return

    def loadModel(self, _a, _b):
        return

    def saveModel(self, _a, _b):
        return
    
    def getPath(self=None):
        return "AIMD"

    def calculateThrottleRate(self, current_load, _):
        # given the through rate, load and iterations per window, what's the % of traffic we let pass

        r_per_iteration = self.rs / self.iterations_per_window * self.seconds_per_window # traffic we allow through each second

        if current_load <= r_per_iteration or r_per_iteration < 0:
            return 0
        else:
            return 1 - (r_per_iteration / current_load)

"""
rate allowed is 5
load is 7

I need to work out (1 - x) * load = allowed

1 - (allowed / load)

7 * (1 - (1 - (5 / 7) ) )
"""


