"""
Replaces main_new, decouples the experiment from the learning agent.

Input: A learning agent

Runs network, sends state to learning agent, gets response, sends response to network.

#BUGS
1) I think my update is wrong as its using the current state not the prior state
and shouldn't it be including both the last state and the prior state?
3) When loading via sarsa (and tensorflow), it doesn't increment the i. Low priority



#TODO



#DONE

1) Made SARSA centralised
2) Made SARSA decentralised
3) Made ddqn decentralised
4) Saved SARSA
5) REMOVED D FROM ACTION LEARNING DDQN, NOT SURE IF THIS HAS GRAVE CONSEQUENCES
6) Ensure the saving and reloading works properly for ALL agents
7) Create script to capture reward per episode as we train
8) Use script for testing purposes. Compare
9) Now pulls correct state
10) Redid network
11) Allow you to choose adversary
"""

from __future__ import division

import numpy as np
import os, sys, logging
from enum import Enum
from network.network_new import *

# list of agents to choose
# from agent.sarsaCentralised import *
from agent.sarsaDecentralised import *
# from agent.ddqnCentralised import *
# from agent.ddqnDecentralised import *

import network.hosts as hostClass

SaveAttackEnum = Enum('SaveAttack', 'random save load')
save_attack_path = "./attack.pkl"


test = False #set to True when testing a trained model
debug = False
load_model = False
save_attack = SaveAttackEnum.load


#if save_attack is SaveAttack.save:

assert(test==load_model) # sanity check to stop myself overwriting past checkpoints



# The class of the adversary to implement
adversary = hostClass.ConstantAttack
# adversary = hostClass.ShortPulse
# adversary = hostClass.MediumPulse
# adversary = hostClass.LargePulse
# adversary = hostClass.GradualIncrease


# Network information
N_state = 3 #The number of state, i.e., the number of filters
N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
action_per_agent = 10 # each filter can do 10 actions
N_switch = 13 # number of routers in the system
hosts_sources = [5, 10, 12, 6, 9, 9] #ID of the switch that the host is connected to  

servers = [0] #ID of the switch that the server is connected to 
filters = [5, 6, 9] #ID of the switch that the filter locates at


batch_size = 32 #How many experiences to use for each training step.
update_freq = 4 #How often to perform a training step.
y = 0 #.99 #Discount factor on the target Q-values

startE = 0.4 #Starting chance of random action
endE = 0.0 #Final chance of random action

assert(action_per_agent**N_state == N_action)

tau = 0.001 #Rate to update target network toward primary network. 


if test:

    num_episodes = 1000
    pre_train_steps = 0
    max_epLength = 60

    e = 0
    stepDrop = 0

    # implement something start attack episode 5 and stop at 55 here

else:

    tau = 0.1
    startE = 0.4
    endE = 0.0

    #num_episodes = 62501
    num_episodes = 2000
    pre_train_steps = 0
    annealing_steps = 50000
    """
    num_episodes = 100001 #How many episodes of game environment to train network with.

    annealing_steps = 60000 #How many steps of training to reduce startE to endE.
    pre_train_steps = 30000 #How many steps of random actions before training begins.

    """
    max_epLength = 30 #The max allowed length of our episode.
    #Set the rate of random action decrease. 
    e = startE
    stepDrop = (startE - endE)/annealing_steps


reward_overload = -1

# J: I think this is lower / upper bounds of message sending by attackers / defenders
rate_legal_low = 0.05 
rate_legal_high = 1 
rate_attack_low = 2.5 
rate_attack_high = 6
legal_probability = 0.6 # probability that is a good guys
upper_boundary = 8



topologyFile = 'topology.txt'

# The network
net = network(N_switch, N_action, N_state, action_per_agent, hosts_sources, servers, filters, reward_overload, 
              rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
              legal_probability, upper_boundary, adversary, max_epLength, topologyFile, SaveAttackEnum, save_attack, save_attack_path)








#create lists to contain total rewards and steps per episode
jList = []
rList = []
loss = []
total_steps = 0
rewards_tampered = 0
experiences_added = 0
largest_gradient = 0
fail = 0



# The learning agent
agent = Agent(N_action, pre_train_steps, action_per_agent, N_state, tau, y, debug, test)


# if debug:
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# else:
#     logging.basicConfig(stream=sys.stderr, level=logging.NOTSET)


name = Agent.getName() # The name of the Agent used
path = agent.getPath() # The path to save model to

load_path = path #ideally can move a good one to a seperate location


#Make a path for our model to be saved in.

if not os.path.exists(path):
    os.makedirs(path)

if test:
    run_mode = "test"
else:
    run_mode = "train"


reward_file = open("{0}/reward-{1}-{2}.csv".format(path,run_mode,adversary.getName()),"w")
loss_file = open("{0}/loss-{1}-{2}.csv".format(path,run_mode,adversary.getName()),"w")
packet_served_file = open("{0}/packet_served-{1}-{2}.csv".format(path,run_mode,adversary.getName()),"w")

print("Using the {0} agent:".format(name))

reward_file.write("Episode,StepsSoFar,TotalReward,LastReward,LengthEpisode,e\n")
packet_served_file.write("Episode,PacketsReceived,PacketsServed,PercentageReceived,ServerFailures\n")


with agent:

    if load_model == True:
        agent.loadModel(load_path)

    for i in range(num_episodes):
        net.reset() # reset the network

        d = False # indicates that network is finished
        rAll = 0 # total reward for system. #TODO shouldn't contribute in pretraining
        j = 0

        while j < max_epLength:
            j+=1

            if j > 1: # when j==1, the actions are chosen randomly, and the state is NULL

                # r = reward, d = episode is done
                d = j==max_epLength
                r = net.calculate_reward()
                rAll += r
                ### why are we putting in the current state??? Shouldn't it be last state
                ### or better, shouldn't it involve both the last state and current state?
                if not test:
                    agent.update(net.last_state, last_action, net.get_state(), d, r)

                if debug:                
                    print("current_state: {0}".format(net.get_state()))
                    print("last state: {0}".format(net.last_state))
                    print("step:" + str(j) + ", action:" + str(last_action) + ", reward:" + str(r), end='\n')
                    print("server state: {0}\n".format(net.switches[0].getWindow()))
                
                    #logging.debug("step: {0} - action: {1} - reward {2}".format(j,last_action,r))
                if r < 0:
                    fail += 1

            #TODO make sure to do do pre_training_stuff
            a = agent.predict(net.get_state(), total_steps, e) # generate an action
            net.step(a, j) # take the action, update the network
            last_action = a 
            total_steps += 1

            if total_steps > pre_train_steps:
                
                if e > endE:
                    e -= stepDrop

                if total_steps % (update_freq) == 0 and not test:
                    l = agent.actionReplay(net.get_state(), batch_size)
                    if l:
                        loss.append(l)

        if i % 1000 == 0:
            print("Completed Episode - {0}".format(i))

        if not test: 
            # save the model only every 10,000 steps
            if i % 10000 == 0:
                agent.saveModel(load_path, i)


        # save data generated
        jList.append(j)
        rList.append(rAll)

        legit_served, legit_all, legit_per, server_failures = net.getLegitStats()
        packet_served_file.write("{0}, {1}, {2}, {3}, {4}\n".format(i, legit_served, legit_all, legit_per, server_failures))

        reward_file.write(str(i) + "," + str(total_steps) + "," + str(rList[-1]) + "," + str(r) + "," + str(jList[-1]) + "," + str(e) + "\n")
        if len(loss) > 0:
            loss_file.write(str(i) + "," + str(total_steps) + "," + str(loss[-1]) + "," + str(e) + "\n")

if save_attack:
    net.save_attacks()

reward_file.close()
loss_file.close()

print("{0} is:".format(name))
print("Percent of succesful episodes: " + str(100 - fail*100/total_steps) + "%")




