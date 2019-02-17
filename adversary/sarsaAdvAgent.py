
import agent.linearSarsaCentralised as linCen


class sarGenAgent(linCen.Agent):
    def __init__(self, N_state, adv_settings, encoders):

        self.leaves = []

        N_action = adv_settings.action_per_agent
        tau = adv_settings.tau
        discount_factor = adv_settings.discount_factor
        




        super().__init__(N_action, N_state, encoders, adv_settings, tau, discount_factor)

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


    def initiate_episode(self):
        self.legal_traffic = 0.0
        self.illegal_traffic = 0.0

        for leaf in self.leaves:
            if leaf.is_attacker:
                self.illegal_traffic+=leaf.traffic_rate
            else:
                self.legal_traffic += leaf.traffic_rate