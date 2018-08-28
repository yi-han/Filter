"""
Replaces main_new, decouples the experiment from the learning agent.

Input: A learning agent

Runs network, sends state to learning agent, gets response, sends response to network.
"""

from __future__ import division

import numpy as np
import os, sys

from network.network_new import *

from agent.sarsaAgent import *


# Network information
#TODO decouple this as well by putting into a class and feeding in?
N_state = 3 #The number of state, i.e., the number of filters
N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
N_switch = 13
hosts = [5, 10, 12, 6, 9, 9] #ID of the switch that the host is connected to  

servers = [0] #ID of the switch that the server is connected to 
filters = [5, 6, 9] #ID of the switch that the filter locates at

# might put some of this different

batch_size = 32 #How many experiences to use for each training step.
update_freq = 4 #How often to perform a training step.
y = 0 #.99 #Discount factor on the target Q-values
startE = 1 #Starting chance of random action
endE = 0.1 #Final chance of random action
annealing_steps = 900000 #How many steps of training to reduce startE to endE.
num_episodes = 150000 #How many episodes of game environment to train network with.
pre_train_steps = 300000 #How many steps of random actions before training begins.
max_epLength = 30 #The max allowed length of our episode.


reward_overload = -1

# J: I think this is lower / upper bounds of message sending by attackers / defenders
rate_legal_low = 0.05 
rate_legal_high = 1 
rate_attack_low = 2.5 
rate_attack_high = 6
legal_probability = 0.6
upper_boundary = 8

topologyFile = 'topology.txt'

net = network(N_switch, N_action, hosts, servers, filters, reward_overload, 
              rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
              legal_probability, upper_boundary, topologyFile)


test = False #set to True when testing a trained model
debug = False


tau = 0.001 #Rate to update target network toward primary network

### TODO put into AGENT
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





#agent = Agent(N_action, test=test, debug=debug, alph = tau, gam=y)
agent = Agent(N_action, pre_train_steps, alph = tau, gam=y, debug=debug, test=test)

name = Agent.getName()
path = "./filter" + name #The path to save our model to.
load_path = ""


#Make a path for our model to be saved in.
if not os.path.exists(path):
    os.makedirs(path)

reward_file = open(path + "/reward" + name + ".csv", "w")
loss_file = open(path + "/loss" + name + ".csv", "w")


for i in range(num_episodes):
    net.reset()

    d = False # indicates that network is finished
    rAll = 0
    j = 0

    while j < max_epLength:
        j+=1
        net.get_state()

        if j > 1: # when j==1, the actions are chosen randomly, and the state is NULL

            # r = reward, d = done
            d, r = net.calculate_reward(d, j)
            rAll += r

            agent.update(net.current_state, last_action, r)
            print('\n' + "step:" + str(j) + ", action:" + str(last_action) + ", reward:" + str(r), end='')
            if r < 0:
                fail += 1


        #TODO make sure to do do pre_training_stuff
        a = agent.predict(net.current_state, total_steps, e) # action

        net.step(a)
        last_action = a
        total_steps += 1

        if total_steps > pre_train_steps:
            if e > endE:
                e -= stepDrop

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




