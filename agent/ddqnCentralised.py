from agent.ddqn import *
import agent.agentBase as aBase
import numpy as np
import os
import sys

class Agent(aBase.Agent):
    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, tau=0.1, discountFactor=0, debug=False, test=False):

        super().__init__(pre_train_steps, debug, test)

        tf.reset_default_graph() # note remove for the decentralised one

        self.mainQN = Qnetwork(N_state, N_action)
        self.targetQN = Qnetwork(N_state, N_action)
        self.init = tf.global_variables_initializer()
        self.saver = tf.train.Saver()
        self.trainables = tf.trainable_variables()
        self.targetOps = updateTargetGraph(self.trainables,tau)
        self.targetOps = updateTargetGraph(self.trainables,tau)
        self.myBuffer = Memory(capacity=300000)
        self.N_action = N_action
        self.y = discountFactor
        self.sess = tf.Session()
    
    def __enter__(self):
        print("about to run")
        #self.sess = tf.Session()
        self.sess.run(self.init)

        # should load model here


    def __exit__(self, type, value, tb):
        print("\n\n__exit__ called\n\n")
        self.sess.close()
        
    def predict(self, state, total_steps, e):
        randomChoice = super().isRandomGuess(total_steps, e)
        #print("I believe i can make {0} actions".format(self.N_action))
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            mainQN = self.mainQN
            action = self.sess.run(mainQN.predict,feed_dict={mainQN.input:[state]})[0]
        return action

    def update(self, last_state, last_action, current_state,d, r, next_action=None):
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
        print("dying ReLU")
        out = self.sess.run(mainQN.Qout,feed_dict={mainQN.input:[current_state]})[0]
        if out[0] == out [1] and out[0] == out [2] and out[0] == out [3] and out[1] == 0:
            
            sys.exit(-1)

        return l

    def loadModel(self, load_path):
        print("Loading Model...")
        ckpt = tf.train.get_checkpoint_state(load_path)
        self.saver.restore(self.sess,ckpt.model_checkpoint_path)


    def saveModel(self, load_path, iteration):
        if not os.path.exists(load_path):
            os.makedirs(load_path)        
        self.saver.save(self.sess, load_path+'/model-'+str(iteration)+'.ckpt')


    def getName():
        return "CentralisedDDQN"

    def getPath(self):
        if self.test:
            prefix="./trained"
        else:
            prefix = "./filter"
        return prefix+Agent.getName()