
import agent.linearSarsaCentralised as linCen


class sarGenAgent(linCen.Agent):
    def __init__(self, N_state, adv_settings, encoders):

        self.leaves = []

        N_action = adv_settings.action_per_agent
        tau = adv_settings.tau
        discount_factor = adv_settings.discount_factor
        




        super().__init__(N_action, N_state, encoders, adv_settings)

    def addLeaves(self, leaves):
        for leaf in leaves:
            assert(not leaf in self.leaves)
            self.leaves.append(leaf)

    def sendTraffic(self, action):
        # we distribute all the legitimate traffic + adversarial traffic
        # legitimate traffic is constant, adversarial traffic is dependent ono action


        # send legitimate traffic
        # legal_per_leaf = self.legal_traffic/len(self.leaves)

        percent_emit = action/10

        # illegal_per_leaf = self.illegal_traffic * percent_emit / len(self.leaves)
        for leaf in self.leaves:
            leaf.sendTraffic(percent_emit)
            # leaf.destination_switch.new_legal += legal_per_leaf
            # leaf.destination_switch.new_illegal += illegal_per_leaf

    def predict(self, state, e, step):
        if not self.leaves[0].isAttackActive(step):
            # if the attack is off return 0
            return 0
        else:
            return super().predict(state, e)
    
    def update(self, last_state, last_action, current_state, d, r, step, next_action=None):
        # Stores an update to the buffer, actual Qlearning is done in action replay
        if not self.leaves[0].isAttackActive(step-1):
            # if the prior step was not an active attack we are to ignore it.
            print("skipping update SHOULDNT HAPPEN {0}".format(step))
            assert(1==2)
            return
        else:
            return super().update(last_state, last_action, current_state, d, r, next_action)

    def initiate_episode(self):
        self.legal_traffic = 0.0
        self.illegal_traffic = 0.0
        self.illegal_traffic_by_host = [] # 
        for leaf in self.leaves:
            if leaf.is_attacker:
                self.illegal_traffic+=leaf.traffic_rate
                self.illegal_traffic_by_host.append(leaf.traffic_rate)
            else:
                self.legal_traffic += leaf.traffic_rate
                self.illegal_traffic_by_host.append(0)
