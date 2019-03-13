"""
This is a generic attacker agent that can be responsible for attacking all/one defenders.

We will then use a generic controller / master. Then allow individual masters be built on top.

"""

from agent.ddqn import *

import numpy as np
import os
import sys
from numpy import random as random
import re

class ddGenAgent():
    def __init__(self, N_state, adv_settings, encoders):

        self.leaves = []

        N_action = adv_settings.action_per_agent
        tau = adv_settings.tau
        discount_factor = adv_settings.discount_factor

        tf.reset_default_graph() # note remove for the decentralised one

        self.N_state = N_state
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


        
    def predict(self, state, e, step):
        if not self.leaves[0].isAttackActive(step):
            # if the attack is off return 0
            return 0
        assert(len(self.leaves)!=0)
        randomChoice = self.isRandomGuess(e)
        #print("I believe i can make {0} actions".format(self.N_action))
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            mainQN = self.mainQN
            action = self.sess.run(mainQN.predict,feed_dict={mainQN.input:[state]})[0]
        return action

    def update(self, last_state, last_action, current_state, d, r, step, next_action=None):
        # Stores an update to the buffer, actual Qlearning is done in action replay
        if not self.leaves[0].isAttackActive(step-1):
            # if the prior step was not an active attack we are to ignore it.
            print("skipping update SHOULDNT HAPPEN {0}".format(step))
            assert(1==2)
            return
        
        self.myBuffer.store(np.array([deep_copy_state(last_state),last_action,r,deep_copy_state(current_state),d,False])) 


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

    def loadModel(self, load_path):
        print("Loading Model...")
        print(load_path)
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


    # def getName(self=None):
    #     return "ddAdvAgent"

    # def getPath(self):
    #     return self.getName()


    def isRandomGuess(self, e):
        # calculate if meant to do choose a random
        return (random.rand(1) < e)


    def addLeaves(self, leaves):
        for leaf in leaves:
            assert(not leaf in self.leaves)
            self.leaves.append(leaf)

    def sendTraffic(self, action, time_step):
        # we distribute all the legitimate traffic + adversarial traffic
        # legitimate traffic is constant, adversarial traffic is dependent ono action


        if not self.leaves[0].isAttackActive(time_step):
            assert(action==0)

        percent_emit = action/10
        for leaf in self.leaves:
            leaf.sendTraffic(percent_emit,time_step)



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

