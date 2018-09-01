"""
Replaces main_new, decouples the experiment from the learning agent.

Input: A learning agent

Runs network, sends state to learning agent, gets response, sends response to network.

#BUGS
1) I think my update is wrong as its using the current state not the prior state
and shouldn't it be including both the last state and the prior state?
2) Bug with pulling the right state from network
3) When loading via sarsa (and tensorflow), it doesn't increment the i. Low priority



#TODO
2) Ensure the saving and reloading works properly for ALL agents
3) Create script to capture reward per episode as we train
4) Use script for testing purposes. Compare

#DONE

1) Made SARSA centralised
2) Made SARSA decentralised
3) Made ddqn decentralised
4) Saved SARSA
5) REMOVED D FROM ACTION LEARNING DDQN, NOT SURE IF THIS HAS GRAVE CONSEQUENCES


"""

from __future__ import division

import numpy as np
import os, sys

from network.network_new import *

# from agent.sarsaCentralised import *
from agent.sarsaDecentralised import *
# from agent.ddqnCentralised import *
# from agent.ddqnDecentralised import *

import network.adversary as adv


test = True #set to True when testing a trained model
debug = False
load_model = True

# adversary = adv.ConstantAttack
adversary = adv.PulseQuick


# Network information
#TODO decouple this as well by putting into a class and feeding in?
N_state = 3 #The number of state, i.e., the number of filters
N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
action_per_agent = 10 # each filter can do 10 actions
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




if test:

    num_episodes = 1000
    pre_train_steps = 0
    max_epLength = 60

    e = 0
    stepDrop = 0

    # implement something start attack episode 5 and stop at 55

else:

    annealing_steps = 900000 #How many steps of training to reduce startE to endE.
    num_episodes = 150000 #How many episodes of game environment to train network with.
    #num_episodes = 15000 #How many episodes of game environment to train network with.
    pre_train_steps = 300000 #How many steps of random actions before training begins.
    #pre_train_steps = 3000 #How many steps of random actions before training begins.

    max_epLength = 30 #The max allowed length of our episode.

    #Set the rate of random action decrease. 
    e = startE
    stepDrop = (startE - endE)/annealing_steps


reward_overload = -1

# J: I think this is lower / upper bounds of message sending by attackers / defenders
rate_legal_low = 0.05  #
rate_legal_high = 1 
rate_attack_low = 2.5 
rate_attack_high = 6
legal_probability = 0.6 # probability that is a good guys
upper_boundary = 8



topologyFile = 'topology.txt'

net = network(N_switch, N_action, hosts, servers, filters, reward_overload, 
              rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
              legal_probability, upper_boundary, adversary, max_epLength, topologyFile)





tau = 0.001 #Rate to update target network toward primary network



#create lists to contain total rewards and steps per episode
jList = []
rList = []
loss = []
total_steps = 0
rewards_tampered = 0
experiences_added = 0
largest_gradient = 0
fail = 0



agent = Agent(N_action, pre_train_steps, action_per_agent, N_state, tau, y, debug, test)





name = Agent.getName()
path = agent.getPath()

#path = "./filter" + name #The path to save our model to.
#load_path = ""
load_path = path #ideally can move a good one to a seperate location


#Make a path for our model to be saved in.

if not os.path.exists(path):
    os.makedirs(path)

reward_file = open(path + "/reward" + name + ".csv", "w")
loss_file = open(path + "/loss" + name + ".csv", "w")
packet_served_file = open(path + "/packet_served" + name+".csv","w")

print("{0} is:".format(name))

reward_file.write("Episode, Steps so far, Total reward, Last reward, Length episode, e\n")
packet_served_file.write("Episode, Packets Received, Packets Served, Percentage Received\n")


with agent:

    if load_model == True:
        agent.loadModel(load_path)


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
                d = j==max_epLength
                r = net.calculate_reward()
                rAll += r
                ### why are we putting in the current state??? Shouldn't it be last state
                ### or better, shouldn't it involve both the last state and current state?
                if not test:
                    agent.update(net.last_state, last_action, net.current_state, d, r)
                #agent.update(net.current_state, last_action, r)
                #print("step:" + str(j) + ", action:" + str(last_action) + ", reward:" + str(r), end='\n')
                if r < 0:
                    fail += 1


            #TODO make sure to do do pre_training_stuff
            a = agent.predict(net.current_state, total_steps, e) # action

            net.step(a, j)
            last_action = a
            total_steps += 1

            if total_steps > pre_train_steps:
                if e > endE:
                    e -= stepDrop

                if total_steps % (update_freq) == 0 and not test:
                    l = agent.actionReplay(net.current_state, batch_size)
                    if l:
                        loss.append(l)

        if not test: 
            if i % 1000 == 0:
                print("Completed Episode - {0}".format(i))
                agent.saveModel(load_path, i)

        jList.append(j)
        rList.append(rAll)

        legit_served, legit_all, legit_per = net.getLegitStats()
        packet_served_file.write("{0}, {1}, {2}, {3}\n".format(i, legit_served, legit_all, legit_per))

        reward_file.write(str(i) + "," + str(total_steps) + "," + str(rList[-1]) + "," + str(r) + "," + str(jList[-1]) + "," + str(e) + "\n")
        if len(loss) > 0:
            loss_file.write(str(i) + "," + str(total_steps) + "," + str(loss[-1]) + "," + str(e) + "\n")


reward_file.close()
loss_file.close()

print("{0} is:".format(name))
print("Percent of succesful episodes: " + str(100 - fail*100/total_steps) + "%")




