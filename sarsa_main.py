# designed to be worked with the ddqn agent

"""
#TODO
1) Confirm that alpha = tau and gamma = discount
2) I think update is in wrong area


"""

from __future__ import division

import numpy as np
import os, sys

from network.network_new import *
from agent.sarsa import *
#import agent.sarsa as sarsa

N_state = 3 #The number of state, i.e., the number of filters
N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
N_switch = 13
hosts = [5, 10, 12, 6, 9, 9] #ID of the switch that the host is connected to  


servers = [0] #ID of the switch that the server is connected to 
filters = [5, 6, 9] #ID of the switch that the filter locates at

reward_overload = -1

# J: I think this is lower / upper bounds of message sending by attackers / defenders
rate_legal_low = 0.05 
rate_legal_high = 1 
rate_attack_low = 2.5 
rate_attack_high = 6

legal_probability = 0.6

upper_boundary = 8

net = network(N_switch, N_action, hosts, servers, filters, reward_overload, 
              rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
              legal_probability, upper_boundary, 'topology.txt')

batch_size = 32 #How many experiences to use for each training step.
update_freq = 4 #How often to perform a training step.
y = 0 #.99 #Discount factor on the target Q-values
startE = 1 #Starting chance of random action
endE = 0.1 #Final chance of random action
annealing_steps = 900000 #How many steps of training to reduce startE to endE.
num_episodes = 150000 #How many episodes of game environment to train network with.
pre_train_steps = 300000 #How many steps of random actions before training begins.
# pre_train_steps = 30 #How many steps of random actions before training begins.
max_epLength = 30 #The max allowed length of our episode.
load_model = False #Whether to load a saved model.


name = "basicSarsa"
path = "./filter" + name #The path to save our model to.
load_path = ""


tau = 0.001 #Rate to update target network toward primary network

test = False #set to True when testing a trained model
debug = False

"""
tf.reset_default_graph()
mainQN = Qnetwork(N_state, N_action)
targetQN = Qnetwork(N_state, N_action)

init = tf.global_variables_initializer()

saver = tf.train.Saver()

trainables = tf.trainable_variables()

targetOps = updateTargetGraph(trainables,tau)
"""
#myBuffer = Memory(capacity=300000)

#Set the rate of random action decrease. 
e = startE
stepDrop = (startE - endE)/annealing_steps

#create lists to contain total rewards and steps per episode
jList = []
rList = []
loss = []
total_steps = 0
rewards_tampered = 0
experiences_added = 0
largest_gradient = 0
fail = 0

#Make a path for our model to be saved in.
if not os.path.exists(path):
    os.makedirs(path)

reward_file = open(path + "/reward" + name + ".csv", "w")
loss_file = open(path + "/loss" + name + ".csv", "w")


agent = Agent(N_action, alph = tau, gam=y)
# with Agent(N_action) as agent:

for i in range(num_episodes): # i is the number of episodes
    net.reset() # reset the network
    agent.reset()
    #agent.reset()
    d = False
    rAll = 0        
    j = 0
    while j < max_epLength:
        j += 1
        net.get_state()

        if j > 1: # if j == 1 its initial therefore random action
            d, r = net.calculate_reward(d, j)
            rAll += r
            agent.update(net.current_state, last_action, r)

            # i think i do the update here
            print('\n' + "step:" + str(j) + ", action:" + str(last_action) + ", reward:" + str(r), end='')
            if r < 0:
                fail += 1

        #Choose an action e-greedily (with e chance of random action) from the Q-network
        if (np.random.rand(1) < e or total_steps < pre_train_steps) and not debug and not test:
            a = np.random.randint(0,N_action)
            rd = True

        else:

            a = agent.makeGuess(net.current_state)
            rd = False

        net.step(a)


        last_action = a
        
        total_steps += 1


        if total_steps > pre_train_steps:
            if e > endE:
                e -= stepDrop

            #if total_steps % (update_freq) == 0 and not test:
                #print("they were doing update here?")
                ### I THINK THEY ARE DOING THE UPDATE HERE 
                # but should be above for sarsa?

        if d:
            break

    jList.append(j)
    rList.append(rAll)

reward_file.write(str(i) + "," + str(total_steps) + "," + str(rList[-1]) + "," + str(jList[-1]) + "," + str(e) + "\n")
if len(loss) > 0:
    loss_file.write(str(i) + "," + str(total_steps) + "," + str(loss[-1]) + "," + str(e) + "\n")



reward_file.close()
loss_file.close()

print("Percent of succesful episodes: " + str(100 - fail*100/total_steps) + "%")