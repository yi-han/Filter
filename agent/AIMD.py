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
from enum import Enum
from network.utility import SECONDS_STANDARD_INTERVAL
from network.utility import INF
class AimdMovesEnum(Enum):
    none = 0
    decrease = 1
    increase = 2
    constant = 3

class AIMDagent():
    def __init__(self, network_settings, agent_settings):
        self.num_throttles = network_settings.N_state
        self.delta = agent_settings.delta # for rate increase
        self.beta = agent_settings.beta # for rate decrease
        self.epsilon = agent_settings.epsilon
        self.upper = network_settings.upper_boundary#* SECONDS_STANDARD_INTERVAL
        self.lower = network_settings.lower_boundary #* SECONDS_STANDARD_INTERVAL
        self.reward_function = agent_settings.reward_function
        self.num_agents = 1
        self.agent_settings = agent_settings

        self.max_rate =  network_settings.rate_attack_high * (len(network_settings.host_sources) - 1 ) + (2 * self.delta)
        #self.activate_rate = (self.upper + self.lower)/2 # 4 is to compensate for 2 second interval where typically would be two
        self.activate_rate = (self.upper+self.lower)/self.num_throttles
        print("delta = {0}".format(self.delta))
        print("beta = {0}".format(self.beta))
        print("epsilon = {0}".format(self.epsilon))
        print("Upper/lower = {0}/{1}".format(self.upper, self.lower))
        print("max rate = {0} activate_rate rate = {1}".format(self.max_rate, self.activate_rate))
    def __enter__(self):
        print("enter the AIMD")
        self.reset_aimd()

    def __exit__(self, type, value, tb):
        print("exit the AIMD")

    # def reset(self):
    #     self.reset_episode()

    def reset_episode(self, net):
        self.reset_aimd()
    
    def reset_aimd(self):
        self.rs = -1 # AIMD off
        self.pLast = -INF # 0 indicates that we aren't tracking as AIMD is off
        self.past_predictions = [[self.max_rate]*self.num_agents]*10
        self.past_moves = [[AimdMovesEnum.none.value]*self.num_agents]*10
        self.latest_state = None

    def predict(self, p, _):
        # treat this as set the rate
        # p is server load
        # we calculate the maximum amount of traffic we allow pass through in a 
        p = p[0]
        # init_rs = self.rs
        p/=2 # we convert a two second interval into a one second interval
        if p > self.upper:
            if self.rs == -1:
                self.rs  = self.activate_rate # used to be upper+lower / self.num_throttles
            else:
                self.rs /= self.beta
            recorded_move = AimdMovesEnum.decrease.value
        elif p < self.lower:
            if self.rs == -1 or abs(p-self.pLast) < self.epsilon:
                # turn AIMD off
                self.rs = -1
                self.pLast = -INF
                recorded_move = AimdMovesEnum.none.value
            else:
                self.pLast = p
                self.rs += self.delta
                recorded_move = AimdMovesEnum.increase.value
        else:
            if self.rs == -1:
                recorded_move = AimdMovesEnum.none.value
            else:
                recorded_move = AimdMovesEnum.constant.value
        
        # print("\n\n\nserver load is {0}, p_last is {3} we had {2} and suggesting {1}".format(p, self.rs, init_rs, old_p))
        if self.rs == -1:
            recorded_rs = self.max_rate
        elif self.rs > self.max_rate:
            print("how did it get that high?")
            print(self.max_rate)
            print(self.rs)
            assert(1==2)
        else:
            recorded_rs = self.rs
        self.past_predictions.pop(0)
        self.past_predictions.append([recorded_rs])
        self.past_moves.pop(0)
        self.past_moves.append([recorded_move])
        # print("we set it as {0} | {1} with a delta of {2}".format(self.rs, recorded_rs, recorded_move))

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

    def update_state(self, net):
        self.latest_state = net.switches[0].get_load()

    def get_state(self):
        return [self.latest_state]

    def get_max_agent_value(self):
        max_agent_value = self.max_rate + self.epsilon # add an epsilon so we never hit the absolute max
        # effectively have the maximum throttle rate be two delta values greater than the max rate possible
        agent_tilings = 8
        print(max_agent_value, agent_tilings)
        return (max_agent_value, 10, agent_tilings)

    def get_move_delta_values(self):
        # special funciton if they happen to be using AIMD variant
        max_agent_value = AimdMovesEnum.constant.value + 1
        # effectively have the maximum throttle rate be two delta values greater than the max rate possible
        agent_tilings = 1
        print(max_agent_value, agent_tilings)
        return (max_agent_value, max_agent_value, agent_tilings)




