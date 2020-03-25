"""

This is a subcomponent of ddAdvGenericMaster representing a learning agent 
that consists of the intelligent attacker.

Each learning agent controls a group of Hosts and directs attacking traffic

Uses tensorflow for Deep Reinforcement Learning agent

"""

from agent.ddqn import *

import numpy as np
import os
import sys
from numpy import random as random
import re
from network.utility import *

class ddGenAgent():
    def __init__(self, N_state, adv_settings, encoders):

        self.leaves = [] # each Host the agent controls

        N_action = adv_settings.action_per_agent 
        tau = adv_settings.tau # learning rate
        discount_factor = adv_settings.discount_factor # discount on future rewards

        tf.reset_default_graph() # initiate tensorflow object

        self.N_state = N_state
        # tensorflow initialisation
        self.mainQN = Qnetwork(N_state, N_action)
        self.targetQN = Qnetwork(N_state, N_action)
        self.init = tf.global_variables_initializer()
        self.saver = tf.train.Saver()
        self.trainables = tf.trainable_variables()
        self.targetOps = updateTargetGraph(self.trainables,tau)
        self.targetOps = updateTargetGraph(self.trainables,tau)
        self.myBuffer = Memory(capacity=300000)
        self.N_action = N_action
        self.y = discount_factor
        self.sess = tf.Session()
    
    def __enter__(self):
        print("sess init ddqnAdvAgent")
        #self.sess = tf.Session()
        self.sess.run(self.init)

        # should load model here


    def __exit__(self, type, value, tb):
        print("\n\nadv __exit__ called\n\n")
        self.sess.close()


        
    def predict(self, state, e, can_attack):
        # given input, choose an attacking action
        if not can_attack:
            # if the attack is off return 0
            return 0
        assert(len(self.leaves)!=0)

        # during exploration agent may make a random move
        randomChoice = self.isRandomGuess(e)
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            mainQN = self.mainQN
            action = self.sess.run(mainQN.predict,feed_dict={mainQN.input:[state]})[0]
        return action

    def update(self, last_state, last_action, current_state, d, r, next_action):
        # Stores an update to the buffer, actual Qlearning is done in action replay

        
        self.myBuffer.store(np.array([deep_copy_state(last_state),last_action,r,deep_copy_state(current_state),d,False])) 


    def actionReplay(self, current_state, batch_size):
        #Below we perform the Double-DQN update to the target Q-values

        tree_idx, trainBatch, ISWeights = self.myBuffer.sample(batch_size) #Get a batch of experiences.
        
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

        #Exit if "dying ReLU" occurs (dead neurons)
        out = self.sess.run(mainQN.Qout,feed_dict={mainQN.input:[current_state]})[0]
        if out[0] == out [1] and out[0] == out [2] and out[0] == out [3] and out[1] == 0:
            print("dying ReLU")
    
            sys.exit(-1)

        return l

    def loadModel(self, load_path):
        print("Loading Model...")
        print(load_path)
        
        if not os.path.exists(load_path):
            return -1
        ckpt = tf.train.get_checkpoint_state(load_path)
        self.saver.restore(self.sess,ckpt.model_checkpoint_path)
        checkpoint_log = open(load_path+"/checkpoint")
        check_line = checkpoint_log.readline()
        checkpoint_log.close()
        m = re.search(r'\d+\D', check_line)

        return int(m.group(0)[:-1])


    def saveModel(self, load_path, iteration):
        if not os.path.exists(load_path):
            os.makedirs(load_path)        
        self.saver.save(self.sess, load_path+'/model-'+str(iteration)+'.ckpt')




    def isRandomGuess(self, e):
        # calculate if meant to do choose a random
        return (random.rand(1) < e)


    def addLeaves(self, leaves):
        # initialisation of episode, attatch Hosts to agent
        # structurally legal Hosts are attatched to the attacker but always emit
        # a constant legal traffic rate
        for leaf in leaves:
            assert(not leaf in self.leaves)
            self.leaves.append(leaf)

    def sendTraffic(self, action):
        # we distribute all the legitimate traffic + adversarial traffic
        # legitimate traffic is constant, adversarial traffic is dependent ono action



        percent_emit = action/10
        for leaf in self.leaves:
            leaf.sendTraffic(percent_emit)



    def initiate_episode(self):
        # initialisation of episode, attatch Hosts to agent
        # structurally legal Hosts are attatched to the attacker but always emit
        # a constant legal traffic rate

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
        self.legal_traffic = KbToMb(self.legal_traffic)
        self.illegal_traffic = KbToMb(self.illegal_traffic)

    def get_host_info(self, host_info_enum):
        # information about each host
        # used for providing statistics of the state of the network
        # to the adversary. We seperate legal and illegal traffic
        output = []
        for leaf in self.leaves:
            if host_info_enum in [advHostInfoEnum.hostRoles, advHostInfoEnum.loadsAndRoles]:
                if leaf.is_attacker:
                    output.append(1)
                else:
                    output.append(0)
            if host_info_enum in [advHostInfoEnum.hostLoads, advHostInfoEnum.loadsAndRoles]:
                output.append(leaf.traffic_rate)
            if host_info_enum == advHostInfoEnum.advLoads:
                if leaf.is_attacker:
                    output.append(leaf.traffic_rate)
                else:
                    output.append(0)
        return output


