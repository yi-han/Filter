"""
Replaces main_new, decouples the experiment from the learning agent.

Input: A learning agent

Runs network, sends state to learning agent, gets response, sends response to network.

#BUGS
1) I think my update is wrong as its using the current state not the prior state
and shouldn't it be including both the last state and the prior state?
3) When loading via sarsa (and tensorflow), it doesn't increment the i. Low priority



#TODO
1)I suspect that if e <1 but step < pretrainign, it might still be not working right
14) I think sarsa (and tensorflow) files will collide in parrelel
15) Name dependent on topology
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
12) Input the settings
13) Slurm parrelel

"""

from __future__ import division

import numpy as np
import os#, sys, logging
from enum import Enum
from network.network_new import *




class Experiment:

    def __init__(self, adversary_class, GeneralSettings, NetworkClass, AgentSettings, twist = ""):
        self.save_attack_path = GeneralSettings.save_attack_path
        #self.is_test = GeneralSettings.test
        self.is_debug = GeneralSettings.debug
        self.save_attack = GeneralSettings.save_attack
        self.save_attack_enum = GeneralSettings.SaveAttackEnum
        self.load_model_enum = GeneralSettings.SaveModelEnum
        self.load_model = GeneralSettings.save_model
        self.adversary_class = adversary_class

        self.network_settings = NetworkClass
        self.agent_settings = AgentSettings

        self.twist = twist


        assert(NetworkClass.action_per_agent**NetworkClass.N_state == NetworkClass.N_action)




    def run(self, prefix):
        N_action = self.network_settings.N_action
        N_state = self.network_settings.N_state
        action_per_agent = self.network_settings.action_per_agent



        # hosts_sources = self.network_settings.hosts_sources
        # servers = self.network_settings.servers
        # filters = self.network_settings.filters
        # topologyFile = self.network_settings.topologyFile
        # rate_legal_low = self.network_settings.rate_legal_low
        # rate_legal_high = self.network_settings.rate_legal_high
        # rate_attack_high = self.network_settings.rate_attack_high
        # legal_probability = self.network_settings.legal_probability
        # upper_boundary = self.network_settings.upper_boundary



        y = self.agent_settings.y
        tau = self.agent_settings.tau
        update_freq = self.agent_settings.update_freq
        batch_size = self.agent_settings.batch_size

        num_episodes = self.agent_settings.num_episodes
        pre_train_steps = self.agent_settings.pre_train_steps
        e = 1 # always start full exploration. Gets overwritten in training
        startE = self.agent_settings.startE
        endE = self.agent_settings.endE
        stepDrop = self.agent_settings.stepDrop
        debug = self.is_debug
        max_epLength = self.agent_settings.max_epLength

        test = self.load_model is self.load_model_enum.test
        if self.load_model is self.load_model_enum.test:
            self.num_episodes = 1000
            self.pre_train_steps = 0
            self.max_epLength = 60
            e = 0
            self.stepDrop = 0


        agent = self.agent_settings.agent(N_action, pre_train_steps, action_per_agent, N_state, tau, y, debug, test)

        reward_overload = -1






        print("\n Prefix {0}".format(prefix))

        # The network
        # net = network(N_switch, N_action, N_state, action_per_agent, hosts_sources, servers, filters, reward_overload, 
        #           rate_legal_low, rate_legal_high, rate_attack_low, rate_attack_high, 
        #           legal_probability, upper_boundary, adversary, max_epLength, topologyFile, SaveAttackEnum, save_attack, save_attack_path)




        net = network(self.network_settings, reward_overload, self.save_attack, self.save_attack_enum, self.save_attack_path, self.adversary_class, max_epLength)
        #create lists to contain total rewards and steps per episode
        stepList = []
        rList = []
        loss = []
        total_steps = 0
        rewards_tampered = 0
        experiences_added = 0
        largest_gradient = 0
        fail = 0 # The total number of fails




        # if debug:
            #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        # else:
        #     logging.basicConfig(stream=sys.stderr, level=logging.NOTSET)


        name = self.agent_settings.agent.getName() # The name of the Agent used
        path =  self.network_settings.name + agent.getPath() + self.twist# The path to save model to
        print("Path is {0}".format(path))
        #path = "/data/projects/punim0621" # for slug
        load_path = path #ideally can move a good one to a seperate location


        #Make a path for our model to be saved in.

        if not os.path.exists(path):
            os.makedirs(path)

        if self.load_model is self.load_model_enum.test:
            run_mode = "test"
        else:
            run_mode = "train"

        # determine reward for a prediction at start of episode, we choose the second step as first step is random
        initial_reward_file = open("{0}/init-reward-{1}-{2}-{3}.csv".format(path,run_mode, self.adversary_class.getName(), prefix),"w")
        reward_file = open("{0}/reward-{1}-{2}-{3}.csv".format(path,run_mode, self.adversary_class.getName(), prefix),"w")
        # Similar to init. Different from reward_file as this is if exploration is 0. Measures how accurate it is at the moment.
        final_reward_file = open("{0}/final-reward-{1}-{2}-{3}.csv".format(path,run_mode, self.adversary_class.getName(), prefix),"w")
        
        loss_file = open("{0}/loss-{1}-{2}-{3}.csv".format(path,run_mode, self.adversary_class.getName(), prefix) ,"w")
        packet_served_file = open("{0}/packet_served-{1}-{2}-{3}.csv".format(path,run_mode, self.adversary_class.getName(), prefix),"w")

        print("Using the {0} agent:".format(name))

        
        reward_file.write("Episode,StepsSoFar,TotalReward,LastReward,LengthEpisode,e\n")
        initial_reward_file.write("Episode,StepsSoFar,LastReward,LengthEpisode,e\n")
        final_reward_file.write("Episode,StepsSoFar,LastReward,LengthEpisode,e\n")

        packet_served_file.write("Episode,PacketsReceived,PacketsServed,PercentageReceived,ServerFailures\n")


        with agent:

            if self.load_model in [self.load_model_enum.test, self.load_model_enum.load]:
                agent.loadModel(load_path)

            fail_seg = 0
            for ep_num in range(num_episodes):
                net.reset() # reset the network

                d = False # indicates that network is finished
                rAll = 0 # accumulative reward for system in the episode. #TODO shouldn't contribute in pretraining
                
                for step in range(max_epLength):
                    #TODO make sure to do do pre_training_stuff
                    a = agent.predict(net.get_state(), total_steps, e) # generate an action
                    net.step(a, step) # take the action, update the network

                    
                    if step > 0: # when step==0, the actions are chosen randomly, and the state is NULL

                        # r = reward, d = episode is done
                        d = (step+1)==max_epLength
                        r = net.calculate_reward()
                        rAll += r
                        ### why are we putting in the current state??? Shouldn't it be last state
                        ### or better, shouldn't it involve both the last state and current state?
                        if not (self.load_model is self.load_model_enum.test):
                            agent.update(net.last_state, last_action, net.get_state(), d, r, next_action = a)


                        if debug:                
                            print("current_state: {0}".format(net.get_state()))
                            print("last state: {0}".format(net.last_state))
                            print("step:" + str(step) + ", action:" + str(last_action) + ", reward:" + str(r), end='\n')
                            print("server state: {0}\n".format(net.switches[0].getWindow()))
                        
                        # if e==endE: # only do this once trained
                        #     print("\n")
                        #     print(net.last_state)
                        #     print(agent.get_action_choices(net.last_state))
                        #     print("step: {0} - action: {1} - reward {2}".format(step,last_action,r))
                        if r < 0:
                            fail += 1
                            fail_seg += 1
                    
                    # if step 1 or final step we want to measure how accurate our system is
                    # to minimise effect on our network we make a prediction then replay the last prior action to undo effect
                    # if step == 1:
                    #     temp_a = agent.predict(net.get_state(), total_steps, 0)
                    #     temp_r = net.virtual_action(temp_a, a, total_steps)
                    #     initial_reward_file.write(str(ep_num) + "," + str(total_steps) + "," + str(temp_r) + "," + str(step) + "," + str(0) + "\n")   
                            
                    last_action = a 
                    
                    total_steps += 1

                    if total_steps > pre_train_steps:
                        #print("e={0} startE = {1}".format(e, startE))
                        if e > startE:
                            e = startE
                        elif e > endE:
                            e -= stepDrop
                        elif e < endE:
                            e = endE


                        if update_freq and not test and total_steps % (update_freq) == 0:
                            l = agent.actionReplay(net.get_state(), batch_size)
                            if l:
                                loss.append(l)

                # record final prediciton with exploraiton at 0
                # if e>0:
                #     temp_a = agent.predict(net.get_state(), total_steps, 0)
                #     net.step(a, step) # take the action, update the network
                #     last_reward = net.calculate_reward()
                # else:
                #     last_reward = r
                # final_reward_file.write(str(ep_num) + "," + str(total_steps) + "," + str(last_reward) + "," + str(step) + "," + str(0) + "\n")   




                if ep_num % 1000 == 0:
                    print("Completed Episode - {0}".format(ep_num))
                    print("E={0} Fails = {1} FailPer = {2}".format(e,fail_seg, (fail_seg*100/(1000*max_epLength))))
                    fail_seg = 0
                if self.load_model is self.load_model_enum.save: 
                    # save the model only every 10,000 steps
                    if ep_num % 10000 == 0:
                        agent.saveModel(load_path, ep_num)


                # save data generated
                stepList.append(step)
                rList.append(rAll)

                legit_served, legit_all, legit_per, server_failures = net.getLegitStats()
                packet_served_file.write("{0}, {1}, {2}, {3}, {4}\n".format(ep_num, legit_served, legit_all, legit_per, server_failures))

                reward_file.write(str(ep_num) + "," + str(total_steps) + "," + str(rList[-1]) + "," + str(r) + "," + str(stepList[-1]) + "," + str(e) + "\n")
                if len(loss) > 0:
                    loss_file.write(str(ep_num) + "," + str(total_steps) + "," + str(loss[-1]) + "," + str(e) + "\n")

        if self.save_attack is self.save_attack_enum.save:
            net.save_attacks()

        reward_file.close()
        loss_file.close()
        initial_reward_file.close()
        final_reward_file.close()

        print("{0} is:".format(name))
        print("Percent of succesful episodes: " + str(100 - fail*100/total_steps) + "%")




