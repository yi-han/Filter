"""
This is an agent for reinforcement adversary.
We will incorporate DDQN however will aim to decouple DDQN from this later


Functions:

1) Make prediction
Input:
    1. Available bandwidth from agent
    2. Available bandwith of all other agents (merge above)
    3. Does not have the current throttling rate
    4. Past three steps. Each agent:
        a. Bandwidth capacity (shouldn't change so probably can remove)
        b. Action ?
        c. Rate throttled per agent ?
        d. Reward for action ?
        e. Throttle of traffic from agent?
    5. Set of actions by prior agents? (skip initially)
Action:
    1. Number from 0 to 10 (inclusive), percentage of traffic used
    2. Update state representation (for past)

2) Update
Input:
    1. State
    2. Action
    3. Reward

3) reset_episode
Action:
    1. reset state represetntation
"""
from agent.ddqn import *

import numpy as np
import os
import sys
from numpy import random as random

class ddAdvAgent():
    def __init__(self, N_state, adv_settings, is_test=False):

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


        self.is_test = is_test
        self.pre_train_steps = adv_settings.pre_train_steps
    
    def __enter__(self):
        print("sess init ddqnAdvAgent")
        #self.sess = tf.Session()
        self.sess.run(self.init)

        # should load model here


    def __exit__(self, type, value, tb):
        print("\n\nadv __exit__ called\n\n")
        self.sess.close()


        
    def predict(self, state, total_steps, e):
        assert(len(self.leaves)!=0)
        randomChoice = self.isRandomGuess(total_steps, e)
        #print("I believe i can make {0} actions".format(self.N_action))
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            mainQN = self.mainQN
            action = self.sess.run(mainQN.predict,feed_dict={mainQN.input:[state]})[0]
        return action

    def update(self, last_state, last_action, current_state, d, r):
        # Stores an update to the buffer, actual Qlearning is done in action replay
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


    def saveModel(self, load_path, iteration):
        if not os.path.exists(load_path):
            os.makedirs(load_path)        
        self.saver.save(self.sess, load_path+'/model-'+str(iteration)+'.ckpt')


    def getName(self=None):
        return "ddAdvAgent"

    def getPath(self):
        return self.getName()


    def isRandomGuess(self, total_steps, e):
        # calculate if meant to do choose a random
        return (random.rand(1) < e or total_steps < self.pre_train_steps) and not self.is_test


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




