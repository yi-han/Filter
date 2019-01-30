"""
The adjacent of an adversarial attacker. We have removed any learning from this model
and assume its decided by its boss.

"""



class ddDumbAgent():
    def __init__(self):

        self.leaves = []



    def addLeaf(self, leaf):
        assert(not leaf in self.leaves)
        self.leaves.append(leaf)

    def sendTraffic(self, action):
        # we distribute all the legitimate traffic + adversarial traffic
        # legitimate traffic is constant, adversarial traffic is dependent ono action


        # send legitimate traffic
        legal_per_leaf = self.legal_traffic/len(self.leaves)

        percent_emit = action/10
        illegal_per_leaf = self.illegal_traffic * percent_emit / len(self.leaves)
        for leaf in self.leaves:
            leaf.destination_switch.new_legal += legal_per_leaf
            leaf.destination_switch.new_illegal += illegal_per_leaf


    def initiate_episode(self):
        self.legal_traffic = 0.0
        self.illegal_traffic = 0.0

        for leaf in self.leaves:
            if leaf.is_attacker:
                self.illegal_traffic+=leaf.traffic_rate
            else:
                self.legal_traffic += leaf.traffic_rate



