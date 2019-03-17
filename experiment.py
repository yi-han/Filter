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

def calculate_e(current_episode, pretraining_episodes, startE, endE, annealing_episodes):
    if current_episode < pretraining_episodes:
        return 1
    elif current_episode >= (pretraining_episodes + annealing_episodes):
        return endE
    elif current_episode == pretraining_episodes:
        return startE
    else:
        percentRemaining = 1 - ((current_episode- pretraining_episodes)/annealing_episodes)
        assert(percentComplete > 0 and percentComplete < 1)
        e = endE + ((startE - endE)*percentRemaining)
        return e

class Experiment:

    def __init__(self, adversary_class, NetworkClass, AgentSettings, oppositionSettings, load_attack_path= None):
        self.load_attack_path = load_attack_path
        self.adversary_class = adversary_class
        self.network_settings = NetworkClass
        self.agent_settings = AgentSettings
        self.representationType = AgentSettings.stateRepresentation
        print(NetworkClass.N_state)
        print(NetworkClass.action_per_throttler**NetworkClass.N_state)
        print(NetworkClass.N_action)
        assert(NetworkClass.action_per_throttler**NetworkClass.N_state == NetworkClass.N_action)

        self.opposition_settings = oppositionSettings


        self.agentLoadModes = [mapsAndSettings.defender_mode_enum.test_short, mapsAndSettings.defender_mode_enum.load, mapsAndSettings.defender_mode_enum.load_save, mapsAndSettings.defender_mode_enum.load_continue]
        self.agentSaveModes = [mapsAndSettings.defender_mode_enum.save, mapsAndSettings.defender_mode_enum.load_save, mapsAndSettings.defender_mode_enum.load_continue]
        self.agentInitialiseMode = [mapsAndSettings.defender_mode_enum.save, mapsAndSettings.defender_mode_enum.load_continue]
        self.agentTestModes = [mapsAndSettings.defender_mode_enum.test_short]

        assert AgentSettings.trained_drift != -1 # ensure we have it set, dont ever use in experiment

    def run(self, prefix, agent, file_path):
        N_action = self.network_settings.N_action
        N_state = self.network_settings.N_state
        action_per_throttler = self.network_settings.action_per_throttler 
        self.file_path = file_path
        update_freq = self.agent_settings.update_freq
        batch_size = self.agent_settings.batch_size
        #create lists to contain total rewards and steps per episode
        stepList = []
        rList = []
        advRList = []
        loss = []
        adv_loss = []
        # determine reward for a prediction at start of episode, we choose the second step as first step is random
        reward_lines = []
        loss_lines = []
        adv_loss_lines = []
        packet_served_lines = []    
        server_actions_lines = [] # file for recording the actions and the moves by actors
        total_steps = 0
        fail = 0 # The total number of fails 
        e = 1 # always start full exploration. Gets overwritten in training
        agent.reset()
        



        """
        Determine the episodes and exploration for the defender

        """

        if self.agent_settings.save_model_mode in self.agentTestModes:
            num_episodes = 500 #500
            max_epLength = 60
        else:
            num_episodes = self.agent_settings.num_episodes
            max_epLength = self.network_settings.max_epLength

        if self.agent_settings.save_model_mode in self.agentInitialiseMode: #self.agentLoadModes:
            pre_train_episodes = self.agent_settings.pre_train_episodes
            step_drop = (self.agent_settings.startE - self.agent_settings.endE)/(self.agent_settings.annealing_episodes*max_epLength)
            # work out e later
        else:
            assert(self.agent_settings.save_model_mode in self.agentLoadModes)
            e = self.agent_settings.endE
            step_drop = 0
            pre_train_episodes = 0


        if self.opposition_settings.is_intelligent:
            # we have a smart advesary. We default to the largest of the number of episodes for defender or attacker
            self.network_settings.is_sig_attack = True # ensure we only have significant attacks when there is an advesary to mimic testing conditions
            assert(self.adversary_class == hosts.adversarialLeaf)
            self.adversarialMaster = self.opposition_settings.adversary_class(self.opposition_settings, self.network_settings, agent.getPath(), agent)

            if self.opposition_settings.save_model_mode in self.agentTestModes:
                assert(self.agent_settings.save_model_mode in self.agentTestModes)
                # if this is true we already have number of episodes set
            else:
                if self.agent_settings.save_model_mode in self.agentSaveModes:
                    num_episodes = max(num_episodes, self.opposition_settings.num_episodes)
                else:
                    num_episodes = self.opposition_settings.num_episodes
                assert(not self.agent_settings.save_model_mode in self.agentTestModes)
            
            if self.opposition_settings.save_model_mode in self.agentInitialiseMode:          
                adv_pretrain_episodes = self.opposition_settings.pre_train_episodes
                adv_step_drop = (self.opposition_settings.startE - self.opposition_settings.endE) / (self.opposition_settings.annealing_episodes  * max_epLength)

            else:
                assert(self.opposition_settings.save_model_mode in self.agentLoadModes)
                adv_pretrain_episodes = 0
                adv_e = self.opposition_settings.endE
                adv_step_drop = 0  


        else:
            self.adversarialMaster =  self.opposition_settings.adversary_class(self.opposition_settings, max_epLength)
            adv_e = 0

        net = self.network_settings.emulator(self.network_settings, self.agent_settings.reward_overload, self.adversary_class, max_epLength, self.representationType, self.agent_settings, self.adversarialMaster, load_attack_path=self.load_attack_path)

        print("Experiment has {0} episodes".format(num_episodes))
        print("\n Prefix {0}".format(prefix))
        print("Path is {0}".format(self.file_path))

        #Make a path for our model to be saved in.

        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)                
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                assert(os.path.exists(file_path))
                pass

        # Similar to init. Different from reward_file as this is if exploration is 0. Measures how accurate it is at the moment.
        
        print("Using the {0} agent:".format(self.agent_settings.name))
        print("Advesary is {0}".format(self.opposition_settings.name))
        print("There are {0} episodes this simulation".format(num_episodes))
        reward_lines.append("Episode,StepsSoFar,TotalReward,LastReward,LengthEpisode,e,PerPacketIdeal,AdvTotalReward,AdvLastReward\n")
        packet_served_lines.append("Episode,LegalReceived,LegalSent,PercentageReceived,ServerFailures,IllegalServed,IllegalSent\n")
        loss_lines.append("Episode,StepsSoFar,Loss,Exploration,EpDefLoss\n")
        #self.episode_rewards = []
        if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
            adv_loss_lines.append("Episode,StepsSoFar,Loss,Exploration,EpDefLoss\n")
        server_actions_line = "Episode,Step,LegalReceived,LegalSent,LegalPercentage,IllegalServed,IllegalSent,TotalSent,LegalCap,IllegalCap,TotalCap,NumAdvesary"

        for i in range(self.network_settings.N_state):
            server_actions_line += ",DefAction{0}".format(i)
        for i in range(self.opposition_settings.num_adv_agents):
            server_actions_line += ",AdvAction{0}".format(i)
        server_actions_line += "\n"
        server_actions_lines.append(server_actions_line)
        ep_init = 0


        with agent:
            self.adversarialMaster.__enter__()
            if self.agent_settings.save_model_mode in self.agentLoadModes : #mapsAndSettings.defender_mode_enum.test
                episode = agent.loadModel(self.file_path, prefix)
                if self.agent_settings.save_model_mode == mapsAndSettings.defender_mode_enum.load_continue:
                    ep_init = episode
            if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentLoadModes:              
                episode = self.adversarialMaster.loadModel(self.file_path, prefix)
                if self.opposition_settings.save_model_mode == mapsAndSettings.defender_mode_enum.load_continue:
                    ep_init = episode

            fail_seg = 0
            adv_last_action = None
            reward_per_print = 0

            # set e for defender
            if self.agent_settings.save_model_mode in self.agentInitialiseMode:
                e = calculate_e(ep_init, pre_train_episodes, self.agent_settings.startE, self.agent_settings.endE, self.agent_settings.annealing_episodes)
            # set e for advesary
            if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentInitialiseMode:
                adv_e = calculate_e(ep_init, adv_pretrain_episodes, self.opposition_settings.startE, self.opposition_settings.endE, self.opposition_settings.annealing_episodes)



            print("\n\n Starting at episode {0}".format(ep_init))
            for ep_num in range(ep_init, num_episodes):
                agent.reset_episode()
                ep_adv_loss = 0
                ep_def_loss = 0
                # print("\n\n\n\nloading ep {0} out of {1}".format(ep_num, num_episodes))
                
                net.reset() # reset the network
                if self.opposition_settings:
                    self.adversarialMaster.initiate_episode()

                d = False # indicates that network is finished
                rAll = 0 # accumulative reward for system in the episode. #TODO shouldn't contribute in pretraining
                
                advRAll = 0 # total reward for episode
                r = 0
                
                if self.network_settings.save_per_step_stats:
                    (legal_capacity, illegal_capacity, total_capacity) = net.getHostCapacity()

                for step in range(max_epLength):

                    adv_state = self.adversarialMaster.get_state(net, adv_e, step, r)
                    adv_action = self.adversarialMaster.predict(adv_state, adv_e, step)

                    a = agent.predict(net.get_state(), e) # generate an action
                    #net.step(a, step) # take the action, update the network
                    
                    if step > 0: # when step==0, the actions are chosen randomly, and the state is NULL

                        # r = reward, d = episode is done
                        d = (step+1)==max_epLength
                        r = net.calculate_reward()
                        rAll += r


                        ### why are we putting in the current state??? Shouldn't it be last state
                        ### or better, shouldn't it involve both the last state and current state?
                        if self.agent_settings.save_model_mode in self.agentSaveModes:
                            agent.update(net.last_state, last_action, net.get_state(), d, r, next_action = a)

                        if self.opposition_settings.is_intelligent:
                            
                            adv_r = self.adversarialMaster.calc_reward(r)
                            if self.opposition_settings.save_model_mode in self.agentSaveModes:
                                self.adversarialMaster.update(adv_last_state, adv_last_action, adv_state, d, adv_r, step, adv_action)
                            self.adversarialMaster.update_past_state(adv_action)
                        else:
                            adv_r = 0

                        advRAll += adv_r
                        #if debug:                
                        # if(net.get_state() != net.last_state):
                        #     print("E = {1} | step = {2} | current_state: {0}".format(net.get_state(), ep_num, step))
                        #     print(r)
                        # elif finished == False:
                        #     print("\n\n\n")
                        #     finished = True
                        # # print("last state: {0}".format(net.last_state))
                        # if ep_num == 0:# or ep_num == 1:
                        #     throttler = net.switches[6]
                        #     throttle_combined = (throttler.legal_window+throttler.dropped_legal_window)
                        #     assert(throttler.is_filter)
                        #     router = net.switches[7]
                        #     below_combined = (router.legal_window+router.dropped_legal_window)
                        #     after = net.switches[4]
                        #     after_combined = (after.legal_window+after.dropped_legal_window)
                        #     further = net.switches[2]
                        #     further_combined = (further.legal_window+further.dropped_legal_window)

                        # if step>1 and abs(throttle_combined + below_combined - further_combined) >10:
                            # print("Ep {0} Step {1}".format(ep_num, step))
                            # print("throttler = {0}".format(throttle_combined))

                            # print("below = {0}".format(below_combined))

                            # print("after = {0}".format(after_combined))

                            # print("further = {0}".format(further_combined))

                        #     print("\n\n")
                        # print("def | step {0} | action {1} | reward {2} | e {3}".format(step, last_action, r, e))
                        # print("state was {0}".format(net.get_state()))
                        # print("experimental load is {0}".format(net.getPacketServedAtMoment()))
                        # print("Bucket load {0}".format(list(map(lambda throttler: throttler.bucket.bucket_load, net.throttlers))))
                        # print("reward was {0}".format(r))
                        #     print("server at {0}".format(net.switches[0].legal_window + net.switches[0].illegal_window))
                        #     #print("adversary | ep {3} | action {0} | reward {1} | e {2}".format(adv_action, r, adv_e, ep_num))
                        #     print(net.switches[3].past_throttles)
                        #     if step==23:
                        #         print("adv_state {0}".format(adv_state))
                               

                                # print("state = {1}, e = {0}".format(e, net.last_state))

                        #     # print("server state: {0}\n".format(net.switches[0].getWindow()))
                        
                        # if step in range(0,8) or step in range(53,57):  
                        #     print("In Episode - {0} Step - {1}".format(ep_num, step))

                        #     print("prio state was {0}".format(net.last_state))
                        #     print("def | step {0} | action {1} | reward {2} | e {3}".format(step, last_action, r, e))
                        #     print("advesary made move {0}".format(adv_action))
                            # if self.adversarialMaster:
                            #     print("adversary | ep {3} | action {0} | reward {1} | adv_e {2}".format(adv_last_action, adv_r, adv_e, ep_num))
                            #     print("adversary_state: {0}".format(adv_last_state))
                            #     print("adv current state: {0} | action {1} \n\n".format(adv_state, adv_action))
                        # if step == 57:
                        #     print("\n\n")

                        if r < 0:
                            fail += 1
                            fail_seg += 1
                    
                    net.step(a, step, adv_action) # take the action, update the network
                    # ideally get rid of double up


                    if self.adversarialMaster != None:
                        adv_last_action = adv_action
                        adv_last_state = adv_state                          
                    
                    last_action = a   
                    total_steps += 1
                    

                    

                    if self.agent_settings.save_model_mode in self.agentSaveModes:
                        if ep_num < pre_train_episodes:
                            e = 1
                        elif e > self.agent_settings.startE:
                            e = self.agent_settings.startE
                        elif e > self.agent_settings.endE:
                            e -= step_drop 
                        elif e < self.agent_settings.endE:
                            #assert(1==3)
                            e = self.agent_settings.endE
                    else:
                        e = self.agent_settings.endE
                    
                    if update_freq and self.agent_settings.save_model_mode in self.agentSaveModes and total_steps % (update_freq) == 0:
                        l = agent.actionReplay(net.get_state(), batch_size)
                        if l:
                            loss.append(l)
                            ep_def_loss += abs(l)


                    if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                        if ep_num < adv_pretrain_episodes:
                            adv_e = 1
                        elif adv_e > self.opposition_settings.startE:
                            adv_e = self.opposition_settings.startE
                        elif adv_e > self.opposition_settings.endE:
                            adv_e -= adv_step_drop 
                        elif adv_e < self.opposition_settings.endE:
                            #assert(1==3)
                            adv_e = self.opposition_settings.endE                    

                        if total_steps % self.opposition_settings.update_freq == 0:
                            adv_l = self.adversarialMaster.actionReplay(adv_state, self.opposition_settings.batch_size)
                            adv_loss.append(adv_l)
                            ep_adv_loss += abs(adv_l)



                    
                    
                    if self.network_settings.save_per_step_stats:
                        (legit_served, legit_sent, legal_per, illegal_served, illegal_sent) = net.getStepPacketStatistics()
                        total_sent = legit_sent+illegal_sent
                        server_actions_line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}".format(ep_num, step, legit_served, legit_sent, legal_per, illegal_served, illegal_sent, total_sent, legal_capacity, illegal_capacity, total_capacity, self.opposition_settings.num_adv_agents)

                        for i in range(self.network_settings.N_state):
                            server_actions_line += ",{0}".format(a[i])
                        for i in range(self.opposition_settings.num_adv_agents):
                            server_actions_line += ",{0}".format(adv_action[i])
                        
                        
                        server_actions_line+= "\n"
                        server_actions_lines.append(server_actions_line)

                #self.episode_rewards.append(net.rewards_per_step) DO LATER

                reward_per_print += rAll
                if ep_num % 1000 == 0:
                    print("Completed Episode - {0}".format(ep_num))
                    print("average reward = {0}".format(reward_per_print/1000/max_epLength*100))
                    reward_per_print = 0
                    print("E={0} Fails = {1} FailPer = {2}".format(e,fail_seg, (fail_seg*100/(1000*max_epLength))))
                    print("def | step {0} | action {1} | reward {2} | e {3}".format(step, last_action, r, e))
                    print("prio state was {0}".format(net.last_state))
                    print("this state was {0}".format(net.get_state()))

                    if self.adversarialMaster:
                        print("adversary | ep {3} | action {0} | reward {1} | adv_e {2}".format(adv_last_action, adv_r, adv_e, ep_num))
                        print("adversary_state: {0}\n".format(adv_last_state))
                    fail_seg = 0
                if ep_num % 10000 == 0:
                    if self.agent_settings.save_model_mode in self.agentSaveModes:  # only save the first iteration 
                        agent.saveModel(self.file_path, ep_num, prefix)
                    if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                        self.adversarialMaster.saveModel(self.file_path, ep_num, prefix)


                # save data generated
                stepList.append(step)
                rList.append(rAll)
                advRList.append(advRAll)
                # grab stats before doing two more
                legit_served, legit_all, legit_per, server_failures, illegal_served, illegal_all = net.getLegitStats()
                
                # for f_step in range(2):
                #     # do two steps without learning (so nothing implicit) and see if we can see how well it performs
                #     a = agent.predict(net.get_state(), 0)
                #     net.step(a, step+f_step, adv_last_action)

                # how well the system performs assuming no exploration (only useful for training)
                agent_performance =  0# we ignore this to reduce timenet.getPacketServedAtMoment()

                packet_served_lines.append("{0},{1},{2},{3},{4},{5},{6}\n".format(ep_num, legit_served, legit_all, legit_per, server_failures, illegal_served, illegal_all))

                reward_lines.append("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(ep_num, total_steps, rList[-1], r, stepList[-1], e, agent_performance, advRList[-1], adv_r))
                if len(loss) > 0:
                    last_loss = loss[-1]
                else:
                    last_loss = 0
                loss_lines.append("{0},{1},{2},{3},{4}\n".format(ep_num,total_steps,last_loss, e, ep_def_loss))
                if self.opposition_settings.is_intelligent and len(adv_loss)>0:
                    last_adv_loss = adv_loss[-1]
                    adv_loss_lines.append("{0},{1},{2},{3},{4}\n".format(ep_num,total_steps,last_adv_loss, e, ep_adv_loss))
            if self.agent_settings.save_model_mode in self.agentSaveModes: # only save the first iteration 
                # save the model only every 10,000 steps
                agent.saveModel(self.file_path, ep_num, prefix)

            if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                self.adversarialMaster.saveModel(self.file_path, ep_num, prefix)

        run_mode = self.agent_settings.save_model_mode.name

        reward_file = open("{0}/reward-{1}-{2}-{3}.csv".format(file_path,run_mode, self.opposition_settings.name, prefix),"w")
        for line in reward_lines:
            reward_file.write(line)
        reward_file.close()

        loss_file = open("{0}/loss-{1}-{2}-{3}.csv".format(file_path,run_mode, self.opposition_settings.name, prefix) ,"w")
        for line in loss_lines:
            loss_file.write(line)
        loss_file.close()
        
        packet_served_file = open("{0}/packet_served-{1}-{2}-{3}.csv".format(file_path,run_mode, self.opposition_settings.name, prefix),"w")
        for line in packet_served_lines:
            packet_served_file.write(line)
        packet_served_file.close()

        if self.opposition_settings.is_intelligent and len(adv_loss)>0:
            opposition_loss_file = open("{0}/adv_loss-{1}-{2}-{3}.csv".format(file_path,run_mode, self.opposition_settings.name, prefix),"w")
            for line in adv_loss_lines:
                opposition_loss_file.write(line)
            opposition_loss_file.close()

        if self.network_settings.save_per_step_stats:
            server_actions_file = open("{0}/server_action_stats-{1}-{2}-{3}.csv".format(file_path,run_mode, self.opposition_settings.name, prefix),"w")
            
            for line in server_actions_lines:
                server_actions_file.write(line)
            server_actions_file.close()



        print("{0} is:".format(self.agent_settings.name))
        print("Percent of succesful episodes: " + str(100 - fail*100/total_steps) + "%")



 

