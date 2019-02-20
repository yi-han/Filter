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
        self.rs = None
        self.pLast = None        

    def predict(self, p, _):
        # treat this as set the rate
        # p is server load
        # we calculate the maximum amount of traffic we allow pass through in a 
        p = p[0][0]
        #init_rs = self.rs

        if p > self.upper:
            if self.rs == None:
                self.rs  = (self.upper + self.lower)/self.num_throttles
            else:
                self.rs /= self.beta
            self.pLast = p
        elif p < self.lower:
            if self.pLast == None or self.rs == None or abs(p - self.pLast) < self.epsilon:
                self.rs = None
                self.pLast = None
            else:
                self.pLast = p
                self.rs += self.delta
        #print("\n\n\nserver load is {0} we had {2} and suggesting {1}".format(p, self.rs, init_rs))
        return self.rs

    def update(self, _, _a, _b, _c, _d, next_action = 0):
        return

    def actionReplay(self, _a, _b):
        return

    def loadModel(self, _a, _b):
        return

    def saveModel(self, _a, _b, _c):
        return
    
    def getPath(self=None):
        return "AIMD"



    # def calculateThrottleRate(self, current_load, current_rs):
    #     # given the through rate, load and iterations per window, what's the % of traffic we let pass

    #     if current_rs == None:
    #         # no throttle set
    #         return 0
    #     r_per_iteration = current_rs / self.iterations_per_window * self.seconds_per_window # traffic we allow through each second

    #     if current_load <= r_per_iteration or r_per_iteration < 0:
    #         return 0
    #     else:
    #         return 1 - (r_per_iteration / current_load)



