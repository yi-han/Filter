from agent.ddqn import *
import agent.agentBase as aBase
import numpy as np



class Agent(aBase.Agent):
    def __init__(self, load_path):
        super().__init__(pre_train_steps, debug, test)

        tf.reset_default_graph() # note remove for the decentralised one

        self.mainQN = Qnetwork(N_state, N_action)
        self.targetQN = Qnetwork(N_state, N_action)
        self.init = tf.global_variables_initializer()
        self.saver = tf.train.Saver()
        self.trainables = tf.trainable_variables()
        self.targetOps = updateTargetGraph(trainables,tau)
        self.targetOps = updateTargetGraph(trainables,tau)
        self.myBuffer = Memory(capacity=300000)

    def __enter__(self):
        self.sess = tf.Session()
        self.sess.run(self.init)


    def __exit__(self, type, value, tb):
        print("\n\n__exit__ called\n\n")
        self.sess.close()
        
    def predict(self, state, total_steps, e):
        randomChoice = super().isRandomGuess(total_steps, e)
        if randomChoice:
            action = np.random.randint(0,self.numActions)
        else:
            mainQN = self.mainQN
            action = self.sess.run(mainQN.predict,feed_dict={mainQN.input:[state]})[0]
        return action

    def update



    def getName():
        return "CentralisedDDQN"