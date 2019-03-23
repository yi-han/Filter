"""
Generic interface for many agents for adversary.
We assign the potentials for each agent randomally each episode
as opposed to using another agent to coordinate the agents.

Comprised of many DDQN networks with one per adversarial agent


"""

from network.utility import advesaryStandardAttackEnum as advAttackEnum
import random

"""
Algorithms to determine attacks

"""



def predict_constant_attack(step):
    return 10

def predict_pulse_generic(step, time_flip):
    time_reduced = step % (2*time_flip) #split episode into two periods

    if time_reduced<time_flip:
        return 10
    else:
        return 0

def predict_pulse_short(step):
    return predict_pulse_generic(step, 1)

def predict_pulse_medium(step):
    return predict_pulse_generic(step, 2)

def predict_pulse_large(step):
    return predict_pulse_generic(step, 5)

def predict_gradual_attack(step, max_epLength):
    percentageAttack = min(2*step/max_epLength,1)
    action = percentageAttack*10
    return action

class dumbMaster():

    def __init__(self, adv_settings, episode_length):
        self.adv_settings = adv_settings
        self.num_adv_agents = adv_settings.num_adv_agents # number of adversarial agents
        self.adv_agents = []

        #assert(self.num_adv_agents == 2)
        for _ in range(self.num_adv_agents):
            self.adv_agents.append(self.adv_settings.adv_agent_class())


        self.all_leaves = [] # list of lists of leaves. Eventually grouped so each inner list corresponds to an adversarial agent
        self.episode_length = episode_length

        self.name = adv_settings.name

    def __enter__(self):
        print("__enter__ dumbMaster ")

        self.assignLeafs()

        for agent in self.adv_agents:

            agent.__enter__()

    def __exit__(self, type, value, tb):
        print("\n\ndumb_master__exit__ called\n\n")
        for agent in self.adv_agents:
            agent.__exit__(type, value, tb)

    def attackStrategyToAction(self, attack_strategy, step):
        """
            Choose the moves for the agents based on algorithm

        """

        if not self.adv_agents[0].leaves[0].isAttackActive(step):
            # action is 0 if it's not an active attack
            return 0

        if attack_strategy == advAttackEnum.constant:

            action = predict_constant_attack(step)
        elif attack_strategy == advAttackEnum.pulse_short:
            action = predict_pulse_short(step)
        elif attack_strategy == advAttackEnum.pulse_medium:
            action = predict_pulse_medium(step)
        elif attack_strategy == advAttackEnum.pulse_large:
            action = predict_pulse_large(step)
        elif attack_strategy == advAttackEnum.gradual:
            action = predict_gradual_attack(step, self.episode_length)            
        else:
            print("attack strategy was {0}".format(attack_strategy))
            assert(1==2)
        return action
 
    def predict(self, state, e, step):
        (strategy1, strategy2) = self.current_strategy
        action1 = self.attackStrategyToAction(strategy1, step)
        action2 = self.attackStrategyToAction(strategy2, step)
        return [action1, action2]


    def sendTraffic(self, actions, step):
        #given the actioons send the traffic
        for i in range(len(self.adv_agents)):
            self.adv_agents[i].sendTraffic(actions[i], step)

    def calc_reward(self, network_reward):
        # convert the network reward to the adversarial reward
        if network_reward<0:
            return 1
        else:
            return 1-network_reward



    def get_state(self, net, e, step):
        return []




    def initiate_episode(self, chosen_strategy = None):
        # here I assume that we know the number of designated attackers
        # The idea is to copy the same probabilty distribution as we had for
        # the normal version. This would be the closest mimic to the training.
        # Another idea is to use an alternate probablity distribution
        

        splitStrategies = [advAttackEnum.constant, advAttackEnum.pulse_short, advAttackEnum.pulse_large]
        # note we left out pulse medium
        random_strategies = [advAttackEnum.constant, advAttackEnum.constant, advAttackEnum.pulse_short, advAttackEnum.pulse_medium, advAttackEnum.pulse_large, advAttackEnum.gradual, advAttackEnum.gradual, advAttackEnum.split]
        
        if chosen_strategy == None:
            chosen_strategy = self.adv_settings.attack_strategy
        if chosen_strategy == advAttackEnum.split: 
            strategy1 = random.choice(splitStrategies)
            splitStrategies.remove(strategy1) # to ensure something different
            strategy2 = random.choice(splitStrategies)
            self.current_strategy = (strategy1, strategy2)
        elif chosen_strategy == advAttackEnum.random:
            # choose a differnt strategy
            chosen_strategy = random.choice(random_strategies)
            return self.initiate_episode(chosen_strategy)
        else:
            # strategy is a constant without any randomness
            self.current_strategy = (chosen_strategy, chosen_strategy)

        

        self.step_count = 0


    def update_past_state(self, actions):
        return

    def update(self, last_state, last_actions, current_state, is_done, reward, step, next_actions):
        return

    def actionReplay(self, current_state, batch_size):

        l = 0

        return l

    def loadModel(self, load_path, prefix):
        # note we are going to use the index of the array as an id
        print("loading all models")
        for i in range(len(self.adv_agents)):
            individual_path = load_path+'/{0}Adv-{1}'.format(i, prefix)
            checkpoint = self.adv_agents[i].loadModel(individual_path)
        return checkpoint

    def saveModel(self,load_path, interation, prefix):
        for i in range(len(self.adv_agents)):
            individual_path = load_path+'/{0}Adv-{1}'.format(i, prefix)
            self.adv_agents[i].saveModel(individual_path, interation)


    def getPath(self):
        return "{0}/{1}".format(self.defender_path,self.name)

    def reset(self):
        assert(1==2) # dont think we use this
        for agent in self.adv_agents:
            agent.reset()



    


    # The following code is abouot assigning leafs to agents

    def addLeaf(self, leaf):
        # add the leaf to the set of leaves we have to assign

        # sanity check
        assert(not [leaf] in self.all_leaves)
        leaf.current_position = leaf.destination_switch
        # # leader is used for grouping the leaves together.
        # # use 
        self.all_leaves.append([leaf])


    def assignLeafs(self):
        """
        Each switch we encounter set a current leader. This ensures past ones catch up and order of priority
        """

        # assign each leaf to an advesarial agent

        k = 0

        switches_seen = {}
        while(len(self.all_leaves)>self.num_adv_agents):
            # keep going until we have as many sets as adversarial agents
            if k >= len(self.all_leaves):
                k = 0
            print("current {0} leaves | {1} agent | {2} k ".format(len(self.all_leaves), self.num_adv_agents, k))


            current_set = self.all_leaves[k]
            leader = current_set[0]

            if leader.current_position in switches_seen:
                associated_set = switches_seen[leader.current_position]
                self.all_leaves.remove(current_set)
                self.all_leaves.remove(associated_set)
                associated_set.extend(current_set)
                self.all_leaves.insert(0, associated_set)

                # remove all traces of this set
                for key in switches_seen:
                    if switches_seen[key]==current_set:
                        switches_seen[key] = associated_set
            else:
                switches_seen[leader.current_position]=current_set
                if leader.current_position.id !=0:
                    # skip as at server
                    leader.current_position = current_set[0].current_position.destination_links[0].destination_switch
                k += 1                
        # sanity check
        assert(len(self.all_leaves)==self.num_adv_agents)
        for i in range(self.num_adv_agents):
            self.adv_agents[i].addLeaves(self.all_leaves[i])
            print("adding {0} leaves to {1}".format(len(self.all_leaves[i]), i))












