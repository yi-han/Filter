
class GenericAdvMaster():

    """
    Common interface enabling smart and dumb attackers to interact with network
    """

    def calculate_reward(self):
        # our reward should be the opposite of the percentage of leggal packets served
        per_served = sum(self.legit_served_hist)/sum(self.legit_sent_hist)
        return 1 - per_served



    def update_reward(self, second, legit_served, legit_sent):
        """
        Keep traf of the reward to provide
        We assume we're calculating every 1 second, but our reward is over 2 seconds
        """
        index = second % 2 
        self.legit_served_hist[index] = legit_served
        self.legit_sent_hist[index] = legit_sent        


    def initiate_episode(self):
        # we assume we update the state every second. We keep track of legal traffic sent/served per window
        self.legit_served_hist = [0]*2
        self.legit_sent_hist = [0]*2

    def sendTraffic(self, actions):
        #given the actioons send the traffic
        for i in range(len(self.adv_agents)):
            self.adv_agents[i].sendTraffic(actions[i])