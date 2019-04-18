"""
Basecase of 0 throttle
"""

import agent.agentBase as aBase

class Agent(aBase.Agent):
    def __init__(self, N_action, N_state, tileFunction, agent_settings):



        self.N_state = N_state
        self.y = agent_settings.discount_factor

    
    def __enter__(self):
        print("sess init noThrottle")
        #self.sess = tf.Session()
        # self.sess.run(self.init)

        # should load model here


    def __exit__(self, type, value, tb):
        print("\n\n__exit__ called\n\n")
        # self.sess.close()
        
    def predict(self, state, e):
        return 0

    def update(self, last_state, last_action, current_state,d, r, next_action):
        # Stores an update to the buffer, actual Qlearning is done in action replay
        return

    def actionReplay(self, current_state, batch_size):


        return 0

    def loadModel(self, load_path):
        return


    def saveModel(self, load_path, iteration):
        return


    def getName(self=None):
        return "NoThrottle"

    def getPath(self):
        return self.getName()