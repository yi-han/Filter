"""
Replaces main_new, decouples the experiment from the learning agent.

Input: A learning agent

Runs network, sends state to learning agent, gets response, sends response to network.

#BUGS
1) I think my update is wrong as its using the current state not the prior state
and shouldn't it be including both the last state and the prior state?
3) When loading via sarsa (and tensorflow), it doesn't increment the i. Low priority



#TODO

16) SaveModelEnum being caleled load_model_enum???
17) Don't thing generic update (actionTo...) is compatible with differnt size agents
18) Why is actionReplay only after pretraining???
19) DOUBLE DOUBLE CHECK THIS IS RIGHT, I THINK THE REWARD IS WRONG
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
1)I suspect that if e <1 but step < pretrainign, it might still be not working right
14) I think sarsa (and tensorflow) files will collide in parrelel
15) Name dependent on topology
"""

from __future__ import division

import numpy as np
import os#, sys, logging
from enum import Enum
from network.network_new import *
import network.hosts as hosts
import mapsAndSettings


class Experiment:

    def __init__(self, adversary_class, NetworkClass, AgentSettings, AdversaryAgentSettings, load_attack_path= None):
        self.load_attack_path = load_attack_path
        self.adversary_class = adversary_class
        self.network_settings = NetworkClass
        self.agent_settings = AgentSettings
        self.representationType = AgentSettings.stateRepresentation
        print(NetworkClass.N_state)
        print(NetworkClass.action_per_throttler**NetworkClass.N_state)
        print(NetworkClass.N_action)
        assert(NetworkClass.action_per_throttler**NetworkClass.N_state == NetworkClass.N_action)

        self.adversary_agent_settings = AdversaryAgentSettings


        self.agentLoadModes = [mapsAndSettings.defender_mode_enum.test_short, mapsAndSettings.defender_mode_enum.load]



    def run(self, prefix, preloaded_agent, file_path):
        N_action = self.network_settings.N_action
        N_state = self.network_settings.N_state
        action_per_throttler = self.network_settings.action_per_throttler
        
        self.file_path = file_path

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
        max_epLength = self.agent_settings.max_epLength 
        agent = preloaded_agent
        agent.reset()


        if self.adversary_agent_settings:
            adv_e = self.adversary_agent_settings.startE
            adv_pretraining = self.adversary_agent_settings.pre_train_steps
            adv_step_drop = (adv_e - self.adversary_agent_settings.endE) / (self.adversary_agent_settings.annealing_episodes  * max_epLength)

            print(self.adversary_class)
            self.adversarialMaster = self.adversary_agent_settings.adversary_class(self.adversary_agent_settings, self.network_settings, agent)
            assert(self.adversary_class == hosts.adversarialLeaf)
        else:
            self.adversarialMaster = None        

        if self.agent_settings.save_model_mode is mapsAndSettings.defender_mode_enum.test_short:
            num_episodes = 500 #500
            pre_train_steps = 0
            max_epLength = 60
            e = 0
            stepDrop = 0
        elif self.agent_settings.save_model_mode is mapsAndSettings.defender_mode_enum.load:
            e = 0
            stepDrop = 0



        run_mode = self.agent_settings.save_model_mode.name
        if self.adversary_agent_settings:
            run_mode = run_mode + "_" + self.adversary_agent_settings.save_model_mode.name
        else:
            run_mode+="_normal"
     

        reward_overload = self.agent_settings.reward_overload
        if reward_overload:
            print("using reward overload")
        print("\n Prefix {0}".format(prefix))
        print("using proper network")
        net = self.network_settings.emulator(self.network_settings, reward_overload, self.adversary_class, max_epLength, self.representationType, self.adversarialMaster, load_attack_path=self.load_attack_path)
        # print("using quick network")
        # net = network_quick(self.network_settings, reward_overload, self.adversary_class, max_epLength, self.representationType, load_attack_path = self.load_attack_path)
        #create lists to contain total rewards and steps per episode
        stepList = []
        rList = []
        loss = []
        total_steps = 0
        rewards_tampered = 0
        experiences_added = 0
        largest_gradient = 0
        fail = 0 # The total number of fails

        name = self.agent_settings.name

        

        print("Path is {0}".format(self.file_path))


        #Make a path for our model to be saved in.

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # determine reward for a prediction at start of episode, we choose the second step as first step is random
        reward_file = open("{0}/reward-{1}-{2}-{3}.csv".format(file_path,run_mode, self.adversary_class.getName(), prefix),"w")
        # Similar to init. Different from reward_file as this is if exploration is 0. Measures how accurate it is at the moment.
        
        loss_file = open("{0}/loss-{1}-{2}-{3}.csv".format(file_path,run_mode, self.adversary_class.getName(), prefix) ,"w")
        packet_served_file = open("{0}/packet_served-{1}-{2}-{3}.csv".format(file_path,run_mode, self.adversary_class.getName(), prefix),"w")
        print("Using the {0} agent:".format(name))
        reward_file.write("Episode,StepsSoFar,TotalReward,LastReward,LengthEpisode,e,PerPacketIdeal\n")
        packet_served_file.write("Episode,PacketsReceived,PacketsServed,PercentageReceived,ServerFailures\n")
        #self.episode_rewards = []


        with agent:
            if self.adversarialMaster:
                self.adversarialMaster.__enter__()
            if self.agent_settings.save_model_mode in self.agentLoadModes: #mapsAndSettings.defender_mode_enum.test
                agent.loadModel(self.file_path)

            if self.adversarialMaster and self.adversary_agent_settings.save_model_mode in self.agentLoadModes:
                self.adversarialMaster.loadModel(self.file_path)

            fail_seg = 0
            adv_last_action = None
            for ep_num in range(num_episodes):
                #print("loading ep {0} out of {1}".format(ep_num, num_episodes))
                net.reset() # reset the network
                if self.adversarialMaster != None:
                    self.adversarialMaster.initiate_episode()

                d = False # indicates that network is finished
                rAll = 0 # accumulative reward for system in the episode. #TODO shouldn't contribute in pretraining
                
                for step in range(max_epLength):
                    #TODO make sure to do do pre_training_stuff
                    # print("my prediction is for {0}".format(net.get_state()))

                    if self.adversarialMaster != None:
                        adv_state = self.adversarialMaster.get_state(net)
                        advAction = self.adversarialMaster.predict(adv_state, total_steps, adv_e)
                    else:
                        advAction = None

                    a = agent.predict(net.get_state(), total_steps, e) # generate an action
                    #net.step(a, step) # take the action, update the network


                    
                    if step > 0: # when step==0, the actions are chosen randomly, and the state is NULL

                        # r = reward, d = episode is done
                        d = (step+1)==max_epLength
                        r = net.calculate_reward()
                        rAll += r
                        ### why are we putting in the current state??? Shouldn't it be last state
                        ### or better, shouldn't it involve both the last state and current state?
                        if not self.agent_settings.save_model_mode in self.agentLoadModes:
                            agent.update(net.last_state, last_action, net.get_state(), d, r, next_action = a)

                        if self.adversarialMaster != None:
                            self.adversarialMaster.update(adv_last_state, adv_last_action, adv_state, d, r)  
                        #if debug:                
                        # print("current_state: {0}".format(net.get_state()))
                        # print("last state: {0}".format(net.last_state))
                        # if step==20:
                        #     print("step:" + str(step) + ", action:" + str(last_action) + ", reward:" + str(r), end='\n')
                        #     print("state = {1}, e = {0}".format(e, net.last_state))
                        # print("server state: {0}\n".format(net.switches[0].getWindow()))
                        
                        if r < 0:
                            fail += 1
                            fail_seg += 1
                    
                    if self.adversarialMaster != None:
                        adv_last_action = advAction
                        adv_last_state = adv_state
                    net.step(a, step, advAction) # take the action, update the network
                    # ideally get rid of double up

                          
                    
                    last_action = a   
                    total_steps += 1
                    
                    if total_steps > pre_train_steps and not self.agent_settings.save_model_mode in self.agentLoadModes:
                        if e > startE:
                            e = startE
                        elif e > endE:
                            e -= stepDrop
                        elif e < endE:
                            e = endE
                            assert(1==2)

                    if update_freq and not self.agent_settings.save_model_mode in self.agentLoadModes and total_steps % (update_freq) == 0:
                        l = agent.actionReplay(net.get_state(), batch_size)
                        if l:
                            loss.append(l)

                    if self.adversarialMaster and not self.adversary_agent_settings.save_model_mode in self.agentLoadModes:
                        if adv_e > self.adversary_agent_settings.startE:
                            adv_e = self.adversary_agent_settings.startE
                        elif adv_e > self.adversary_agent_settings.endE:
                            adv_e -= adv_step_drop 
                        elif adv_e < self.adversary_agent_settings.endE:
                            assert(1==2)
                        if total_steps % self.adversary_agent_settings.update_freq == 0:
                            adv_loss = self.adversarialMaster.actionReplay(adv_state, self.adversary_agent_settings.batch_size)
                #self.episode_rewards.append(net.rewards_per_step) DO LATER






                if ep_num % 1000 == 0:
                    print("Completed Episode - {0}".format(ep_num))
                    print("E={0} Fails = {1} FailPer = {2}".format(e,fail_seg, (fail_seg*100/(1000*max_epLength))))
                    fail_seg = 0
                if prefix == 0 and ep_num % 10000 == 0:
                    if self.agent_settings.save_model_mode is mapsAndSettings.defender_mode_enum.save:  # only save the first iteration 
                        agent.saveModel(self.file_path, ep_num)
                    if self.adversarialMaster and self.adversary_agent_settings.save_model_mode is mapsAndSettings.defender_mode_enum.save:
                        self.adversarialMaster.saveModel(self.file_path, ep_num)


                # save data generated
                stepList.append(step)
                rList.append(rAll)

                # grab stats before doing two more
                legit_served, legit_all, legit_per, server_failures = net.getLegitStats()
                
                for f_step in range(2):
                    # do two steps without learning (so nothing implicit) and see if we can see how well it performs
                    a = agent.predict(net.get_state(), total_steps, 0)
                    net.step(a, step+f_step, adv_last_action)

                # how well the system performs assuming no exploration (only useful for training)
                agent_performance = net.getPacketServedAtMoment()

                packet_served_file.write("{0}, {1}, {2}, {3}, {4}\n".format(ep_num, legit_served, legit_all, legit_per, server_failures))

                reward_file.write("{0},{1},{2},{3},{4},{5},{6}\n".format(ep_num, total_steps, rList[-1], r, stepList[-1], e, agent_performance))
                if len(loss) > 0:
                    loss_file.write(str(ep_num) + "," + str(total_steps) + "," + str(loss[-1]) + "," + str(e) + "\n")


            if prefix == 0:
                if self.agent_settings.save_model_mode is mapsAndSettings.defender_mode_enum.save: # only save the first iteration 
                    # save the model only every 10,000 steps
                    agent.saveModel(self.file_path, ep_num)

                if self.adversarialMaster and self.adversary_agent_settings.save_model_mode is mapsAndSettings.defender_mode_enum.save:
                    self.adversarialMaster.save()

        reward_file.close()
        loss_file.close()

        print("{0} is:".format(name))
        print("Percent of succesful episodes: " + str(100 - fail*100/total_steps) + "%")



 

