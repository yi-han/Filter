"""
Here we have a single master agent in charge of all leaves.

Assume everything moves same level


"""

import math
import adversary.ddDumbAgent as ddDumbAgent
import numpy as np
from numpy import random as random
import sys
import os
from agent.ddqn import *

class CoordinatedAdvMaster():

    def __init__(self, adv_settings, network_setting, defender_path):

        self.prior_agent_actions = 1

        self.pre_train_steps = adv_settings.pre_train_steps
        self.N_action = adv_settings.action_per_agent
        self.tau = adv_settings.tau
        self.discount_factor = adv_settings.discount_factor
        self.update_freq = adv_settings.update_freq
        self.batch_size = adv_settings.batch_size

        self.num_agents = network_setting.N_state



        self.network_setting = network_setting 


        self.agents = []
        self.defender_path = defender_path

        N_adv_state = self.num_agents*(self.prior_agent_actions+1)+3 # plus one due to bandwiths
        for _ in range(self.num_agents):
            self.agents.append(ddDumbAgent.ddDumbAgent())

        self.unassignedAgents = self.agents.copy() # hopefully we copy the references
        self.throttlerLeafDic = {}

        tf.reset_default_graph() # note remove for the decentralised one


        N_action =  self.N_action
        N_state = N_adv_state

        self.N_state = N_adv_state
        self.mainQN = Qnetwork(N_state, N_action)
        self.targetQN = Qnetwork(N_state, N_action)
        self.init = tf.global_variables_initializer()
        self.saver = tf.train.Saver()
        self.trainables = tf.trainable_variables()
        self.targetOps = updateTargetGraph(self.trainables,self.tau)
        self.targetOps = updateTargetGraph(self.trainables,self.tau)
        self.myBuffer = Memory(capacity=300000)
        self.N_action = N_action
        self.y = self.discount_factor
        self.sess = tf.Session()        

    def __enter__(self):
        print("__enter__ CoordinatedAdvMaster decentralised")
        for agent in self.agents:
            #agent.__enter__()
            agent.sess = tf.Session()
            #agent.sess.run(agent.init)
        self.sess.run(self.init)


    def __exit__(self, type, value, tb):
        print("\n\nmaster__exit__ called\n\n")
        self.sess.close()

        # for agent in self.agents:
        #     agent.__exit__(type, value, tb)

    def predict(self, state, e):
        """
            only provide each agent with its corresponding state
            instead of combining the actions into a single action 
            lets use an array.

            Here we just calculate the % of traffic from capacity each agent produces

        """
        randomChoice = self.isRandomGuess(e)
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            mainQN = self.mainQN
            action = self.sess.run(mainQN.predict,feed_dict={mainQN.input:[state]})[0]
        actions = self.action_to_actions(action)

        # print("\nPrediction{0} {1}".format(state, actions))
        return actions

    def sendTraffic(self, actions):
        #given the actioons send the traffic
        for i in range(len(self.agents)):
            self.agents[i].sendTraffic(actions[i])

    def calc_reward(self, network_reward):
        # convert the network reward to the adversarial reward
        if network_reward<0:
            return 1
        else:
            return 1-network_reward



    def get_state(self, net):
        """ 
        Provide the bandwidth capacity for each agent,
        and bandwidth emmitted by each agent over last 3 steps
        last 3 
        """
        assert(len(self.prior_actions) == 3)
        
        # print("\n\n")
        state = self.bandwidths.copy() # start off with bandwidths
        # print(state)
        # print(self.prior_actions)
        state.extend(self.prior_actions)


        # pThrottles = []
        for throttler in net.throttlers:
            state.extend(throttler.past_throttles[-self.prior_agent_actions:])
        #     pThrottles.append(throttler.past_throttles)
        # print(pThrottles)
        
        return np.array(state)

    def initiate_episode(self):
        # here I assume that we know the number of designated attackers
        # The idea is to copy the same probabilty distribution as we had for
        # the normal version. This would be the closest mimic to the training.
        # Another idea is to use an alternate probablity distribution
        
        self.step_count = 0
        self.prior_actions = []
        for _ in range(3): #num past experiences
            self.prior_actions.append(0)
        self.bandwidths= [] # list of the traffic agent can emmit

        for i in range(len(self.agents)):
            self.agents[i].initiate_episode() # just calculating the bandwidths
            self.bandwidths.append(self.agents[i].illegal_traffic)
        # for i in range(len(attackers_per_host)):
        #     attackers = attackers_per_host[i]
        #     for _ in range(attackers):
        #         # repeat each number of attackers
        #         self.bandwidths[i] += self.min_bandwidth + np.random.rand()*(self.max_bandwidth - self.min_bandwidth)


    def update_past_state(self, actions):
        # we note that all the actions are the same, therefore we will shorten this to one
        action = self.actions_to_action(actions)
        self.prior_actions.pop(0)
        self.prior_actions.append(action)
        # print("appending {0}".format(action))

    def update(self, last_state, last_actions, current_state, is_done, adv_reward):
        # provide the update function to each individual state
        # reward = self.calc_reward(network_reward)

        last_action = self.actions_to_action(last_actions)

        self.myBuffer.store(np.array([deep_copy_state(last_state),last_action,adv_reward,deep_copy_state(current_state),is_done,False])) 

        
        # print("Update {0} {1}".format(last_state, last_actions))
        # self.update_past_state(last_actions)

    def actionReplay(self, current_state, batch_size):
        tree_idx, trainBatch, ISWeights = self.myBuffer.sample(batch_size) #Get a batch of experiences.
        #Below we perform the Double-DQN update to the target Q-values
        
        mainQN = self.mainQN
        targetQN = self.targetQN
        batch = np.vstack(trainBatch[:,3])

        Q1 = self.sess.run(mainQN.predict,feed_dict={mainQN.input:batch})
        Q2 = self.sess.run(targetQN.Qout,feed_dict={targetQN.input:batch})
        end_multiplier = -(trainBatch[:,4] - 1)
        doubleQ = Q2[range(batch_size),Q1]
        targetQ = trainBatch[:,2] + (self.y*doubleQ * end_multiplier)

        _, abs_errors, l = self.sess.run([mainQN.updateModel, mainQN.abs_errors, mainQN.loss], \
            feed_dict={mainQN.input:np.vstack(trainBatch[:,0]), mainQN.targetQ:targetQ, mainQN.actions:trainBatch[:,1], mainQN.ISWeights:ISWeights}) #
        
        updateTarget(self.targetOps,self.sess) #Update the target network toward the primary network.
        self.myBuffer.batch_update(tree_idx, abs_errors)

        #Exit if "dying ReLU" occurs
        out = self.sess.run(mainQN.Qout,feed_dict={mainQN.input:[current_state]})[0]
        if out[0] == out [1] and out[0] == out [2] and out[0] == out [3] and out[1] == 0:
            print("dying ReLU")
    
            sys.exit(-1)

        return l

    def loadModel(self, load_path, prefix):
        # note we are going to use the index of the array as an id
        print("loading centralised adversary")
        load_path += "/ddAdvMaster-{0}".format(prefix)
        print(load_path)
        ckpt = tf.train.get_checkpoint_state(load_path)
        self.saver.restore(self.sess,ckpt.model_checkpoint_path)        


    def saveModel(self,load_path, iteration, prefix):
        load_path += "/ddAdvMaster-{0}".format(prefix)
        if not os.path.exists(load_path):
            os.makedirs(load_path)        
        self.saver.save(self.sess, load_path+'/model-'+str(iteration)+'.ckpt')



    def getPath(self):
        return "{0}/smartAdversary".format(self.defender_path)




    


    # The following code is abouot assigning leafs to agents

    def assignLeaf(self, leaf):
        # assign a leaf to an agent

        assert(not leaf in self.throttlerLeafDic.values())

        current_switch = leaf.destination_switch

        while(current_switch.is_filter==False):
            current_switch = current_switch.destination_links[0].destination_switch

        if not current_switch in self.throttlerLeafDic:
            self.throttlerLeafDic[current_switch] = self.unassignedAgents.pop()

        self.throttlerLeafDic[current_switch].addLeaf(leaf)

    def isRandomGuess(self, e):
        # calculate if meant to do choose a random
        return (random.rand(1) < e)



    def actions_to_action(self, actions):
        # technically we are sending a set of actions but it's really the same aciton X times
        assert(actions[0]==actions[-1])
        return actions[0]

    def action_to_actions(self, action):
        actions = [action]
        return self.num_agents*actions






