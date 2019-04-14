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
5) REMOVED D fromOM ACTION LEARNING DDQN, NOT SURE IF THIS HAS GRAVE CONSEQUENCES
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
#import network.network_new as network
import network.hosts as hosts
import network.utility as utility
import mapsAndSettings
import errno

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

class attack_delay_mode(Enum):
    no_delay = 0 # used for training defender
    delay_start = 1 # used for training adversary
    delay_both_sides = 2 # used for evaluation

    


class Experiment:

    def __init__(self, adversary_class, NetworkClass, AgentSettings, oppositionSettings, load_attack_path= None):
        self.load_attack_path = load_attack_path
        self.adversary_class = adversary_class
        self.network_settings = NetworkClass
        self.defender_settings = AgentSettings
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
        update_freq = self.defender_settings.update_freq
        batch_size = self.defender_settings.batch_size
        #create lists to contain total rewards and steps per episode
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
        fail = 0 # The total number of fails 
        e = 1 # always start full exploration. Gets overwritten in training
        
        
        self.delay_attacks = False


        """
        Determine the episodes and exploration for the defender

        """

        if self.defender_settings.save_model_mode in self.agentTestModes:
            num_episodes = 500 #500
            ep_length = self.network_settings.ep_length*2
            self.delay_attacks = True
        else:
            num_episodes = self.defender_settings.num_episodes
            ep_length = self.network_settings.ep_length

        if self.defender_settings.save_model_mode in self.agentInitialiseMode: #self.agentLoadModes:
            pre_train_episodes = self.defender_settings.pre_train_episodes
            step_drop = (self.defender_settings.startE - self.defender_settings.endE)/(self.defender_settings.annealing_episodes)
            # work out e later
        else:
            assert(self.defender_settings.save_model_mode in self.agentLoadModes)
            e = self.defender_settings.endE
            step_drop = 0
            pre_train_episodes = 0


        if self.opposition_settings.is_intelligent:
            # we have a smart advesary. We default to the largest of the number of episodes for defender or attacker
            self.network_settings.is_sig_attack = True # ensure we only have significant attacks when there is an advesary to mimic testing conditions
            self.delay_attacks = True
            assert(self.adversary_class == hosts.adversarialLeaf)
            self.adversarialMaster = self.opposition_settings.adversary_class(self.opposition_settings, self.network_settings, agent.getPath(), agent)

            if self.opposition_settings.save_model_mode in self.agentTestModes:
                assert(self.defender_settings.save_model_mode in self.agentTestModes)
                # if this is true we already have number of episodes set
            else:
                if self.defender_settings.save_model_mode in self.agentSaveModes:
                    num_episodes = max(num_episodes, self.opposition_settings.num_episodes)
                else:
                    num_episodes = self.opposition_settings.num_episodes
                assert(not self.defender_settings.save_model_mode in self.agentTestModes)
            
            if self.opposition_settings.save_model_mode in self.agentInitialiseMode:          
                adv_pretrain_episodes = self.opposition_settings.pre_train_episodes
                adv_step_drop = (self.opposition_settings.startE - self.opposition_settings.endE) / (self.opposition_settings.annealing_episodes)

            else:
                assert(self.opposition_settings.save_model_mode in self.agentLoadModes)
                adv_pretrain_episodes = 0
                adv_e = self.opposition_settings.endE
                adv_step_drop = 0  


        else:
            self.adversarialMaster =  self.opposition_settings.adversary_class(self.opposition_settings, ep_length)
            adv_e = 0

        net = self.network_settings.emulator(self.network_settings, self.defender_settings.reward_overload, self.adversary_class, self.representationType, self.defender_settings, self.adversarialMaster, load_attack_path=self.load_attack_path)

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
        
        print("Using the {0} agent:".format(self.defender_settings.name))
        print("Advesary is {0}".format(self.opposition_settings.name))
        print("There are {0} episodes this simulation".format(num_episodes))
        reward_lines.append("Episode,TotalReward,LastReward,LengthEpisode,e,AdvTotalReward,AdvLastReward\n")
        packet_served_lines.append("Episode,LegalReceived,LegalSent,PercentageReceived,IllegalServed,IllegalSent\n")
        loss_lines.append("Episode,Loss,Exploration,EpDefLoss\n")
        #self.episode_rewards = []
        if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
            adv_loss_lines.append("Episode,Loss,Exploration,EpDefLoss\n")
        server_actions_line = "Episode,Second,LegalReceived,LegalSent,LegalPercentage,IllegalServed,IllegalSent,TotalServed,TotalSent,AssociatedReward,LegalCap,IllegalCap,TotalCap,NumAdvesary"


        ep_init = 0


        with agent:
            # different number of predicitons depending if aimd or rt
            for i in range(agent.num_predictions):
                server_actions_line += ",DefAction{0}".format(i)
            for i in range(self.opposition_settings.num_adv_agents):
                server_actions_line += ",AdvAction{0}".format(i)
            server_actions_line += "\n"
            server_actions_lines.append(server_actions_line)

            self.adversarialMaster.__enter__()
            if self.defender_settings.save_model_mode in self.agentLoadModes : #mapsAndSettings.defender_mode_enum.test
                episode = agent.loadModel(self.file_path, prefix)
                if self.defender_settings.save_model_mode == mapsAndSettings.defender_mode_enum.load_continue:
                    ep_init = episode
            if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentLoadModes:              
                episode = self.adversarialMaster.loadModel(self.file_path, prefix)
                if self.opposition_settings.save_model_mode == mapsAndSettings.defender_mode_enum.load_continue:
                    ep_init = episode

            #adv_past_action = None
            reward_per_print = 0
            reward_print_count = 0
            


            # set e for defender
            if self.defender_settings.save_model_mode in self.agentInitialiseMode:
                e = calculate_e(ep_init, pre_train_episodes, self.defender_settings.startE, self.defender_settings.endE, self.defender_settings.annealing_episodes)
            # set e for advesary
            if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentInitialiseMode:
                adv_e = calculate_e(ep_init, adv_pretrain_episodes, self.opposition_settings.startE, self.opposition_settings.endE, self.opposition_settings.annealing_episodes)
            
        


            """
            Determine how often an agent makes a move
            """            

            defender_move = self.network_settings.iterations_between_second / self.defender_settings.actions_per_second
            adversary_move = self.network_settings.iterations_between_second / self.opposition_settings.actions_per_second

            agent_last_move = (ep_length / defender_move) - 1
            adversary_last_move = (ep_length / adversary_move) - 1
            
            #assert(defender_move == 200 and adversary_move == 200) # we can get rid of this later
            adversary_reward = None
            print("\n\n Starting at episode {0}".format(ep_init))
            print("num_episodes {0} episode length {1} iterations between each second {2}".format(num_episodes, ep_length, self.network_settings.iterations_between_second))
            for ep_num in range(ep_init, num_episodes):
                # print(ep_num)
                agent.reset_episode(net)
                ep_adv_loss = 0
                ep_def_loss = 0
                # print("\n\n\n\nloading ep {0} out of {1}".format(ep_num, num_episodes))
                num_defender_moves = 0
                num_adversary_moves = 0                
                net.reset() # reset the network
                if self.opposition_settings:
                    self.adversarialMaster.initiate_episode()

                rAll = 0 # accumulative reward for system in the episode. #TODO shouldn't contribute in pretraining
                
                advRAll = 0 # total reward for episode
                
                if self.network_settings.save_per_step_stats:
                    (legal_capacity, illegal_capacity, total_capacity) = net.getHostCapacity()
                # Using the network for this
                # legit_served_ep = 0
                # legit_sent_ep = 0
                # illegal_served_ep = 0
                # illegal_sent_ep = 0

                adv_next_state = None
                adv_next_action = None
                
                def_next_state = None
                def_next_action = None
                # episode_steps = ep_length * self.network_settings.iterations_between_second
             
                step = -1
                for second in range(ep_length):
                    # print(second)
                    for iteration in range(self.network_settings.iterations_between_second):
                        step += 1


                        # agent moves
                        if step % adversary_move == 0:
                            adv_step = step/adversary_move # the step for the adversary
                            
                            adv_past_state = adv_next_state
                            adv_past_action = adv_next_action

                            adv_next_state = self.adversarialMaster.get_state(net, adv_e, adv_step)
                            adv_next_action = self.adversarialMaster.predict(adv_next_state, adv_e, adv_step, self.can_attack(second))
                            num_adversary_moves += 1
                            

                        
                            if self.opposition_settings.is_intelligent and num_adversary_moves > 1:
                                adversary_reward = self.adversarialMaster.calculate_reward()
                                advRAll += adversary_reward  
                                if self.opposition_settings.save_model_mode in self.agentSaveModes:
                                    adversary_done = False
                                    if self.can_attack(second-1):
                                        # if the adversary couldn't attack last turn we don't want to update
                                        self.adversarialMaster.update(adv_past_state, adv_past_action, adv_next_state, adversary_done, adversary_reward, adv_next_action) # num_adversary_moves ?
                                
                                
                                        if num_adversary_moves % self.opposition_settings.update_freq == 0:
                                            adv_l = self.adversarialMaster.actionReplay(adv_next_state, self.opposition_settings.batch_size)
                                            adv_loss.append(adv_l)
                                            ep_adv_loss += abs(adv_l)


                                self.adversarialMaster.update_past_state(adv_next_action)





                        if step % defender_move == 0:
                            #print("step {0} defender_cut {1} move {2}".format(step, defender_move, num_defender_moves))
                            #print("made move {0}".format(num_defender_moves))
                            def_step = step/defender_move
                            
                            def_last_state = def_next_state
                            def_past_action = def_next_action

                            agent.calculate_state(net)
                            def_next_state = agent.get_state()
                            def_next_action = agent.predict(def_next_state, e) # generate an action
                            num_defender_moves += 1
                            
                            # print("made prediction {0}".format(def_next_action))
                            if num_defender_moves > 1:

                                """
                                We assume this is only for training.
                                We also assume that during training our reward is calculated over last 2 seconds
                                """
                                defender_reward = net.get_reward()

                                # print("\nlast_state {0} last_prediction {1} current_action {2}".format(def_last_state, def_past_action, def_current_action))
                                # print("New State {1} AssociatedReward {0} ".format(defender_reward, def_next_state))
                                rAll += defender_reward
                                reward_print_count += 1
                                if self.defender_settings.save_model_mode in self.agentSaveModes:



                                    # print("p_state {0} p_action {1} reward {2} n_state {3} n_action {4}".format(def_last_state, def_past_action, defender_reward,def_next_state, def_next_action))
                                    agent_done = False
                                    agent.update(def_last_state, def_past_action, def_next_state, agent_done, defender_reward, def_next_action)


                                    if num_defender_moves % update_freq == 0:
                                        l = agent.actionReplay(def_next_state, batch_size)
                                        if l:
                                            loss.append(l)
                                            ep_def_loss += abs(l)


                                

                            
                            

                        
                        


                        # network makes moves
                        # print("step {0} defender {1} adversary {2}".format(step, def_next_action, adv_next_action))
                        net.simulate_traffic(def_next_action, adv_next_action, step)
                        def_current_action = def_next_action
                        adv_current_action = adv_next_action
                        # print("simulated the move")
                
                    """
                    At the end of every second we record the percentage of traffic that was serviced by the server 

                    """
                    # print("testing actions {0}".format(def_current_action))
                    (legit_served, legit_sent, legal_per, illegal_served, illegal_sent) = net.updateEpisodeStatistics(second)
                    self.adversarialMaster.update_reward(second, legit_served, legit_sent)
                    # if num_defender_moves > 1:
                    #     total_sent = legit_sent+illegal_sent
                    #     print("\nState was {0}".format(def_last_state))
                    #     print("ep_num-move {0}-{1} | def_action {2} | adv_action {3} | per {4}".format(ep_num, num_defender_moves, def_current_action, adv_current_action, legal_per))
                    #     print("ServerState is {0} | Overflow = {1}".format(total_sent, total_sent>16))
                    if self.network_settings.save_per_step_stats:
                        total_sent = legit_sent+illegal_sent

                        total_served = legit_served+illegal_served
                        reward_window = net.get_reward()
                        server_actions_line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}".format(ep_num, second, legit_served, legit_sent, legal_per, illegal_served, illegal_sent, total_served, total_sent, reward_window,legal_capacity, illegal_capacity, total_capacity, self.opposition_settings.num_adv_agents)

                        if isinstance(def_current_action, list):
                            for i in range(self.network_settings.N_state):
                                server_actions_line += ",{0}".format(def_current_action[i])
                        else:
                            server_actions_line += ",{0}".format(def_current_action)
                        for i in range(self.opposition_settings.num_adv_agents):
                            server_actions_line += ",{0}".format(adv_current_action[i])

                        server_actions_line+= "\n"
                        server_actions_lines.append(server_actions_line)


                """
                This is where you would do the 'isDone logic'

                if self.defender_settings.save_model_mode in self.agentSaveModes:
                    print("p_state {0} p_action {1} reward {2} n_state {3} n_action {4}".format(def_last_state, def_past_action, defender_reward,def_next_state, def_next_action))
                    agent_done = True
                    agent.update(def_last_state, def_past_action, def_next_state, agent_done, defender_reward, def_next_action)


                """



                # end of an episode we record some statistics
                rList.append(rAll)
                advRList.append(advRAll)
                reward_per_print += rAll

                if ep_num % 1000 == 0:
                    print("\n\nCompleted Episode - {0}".format(ep_num))
                    print("average reward = {0}".format((reward_per_print/reward_print_count)*100))
                    #print("average Per = {0}".format(t_packet_received/t_packet_sent))
                    reward_per_print = 0
                    reward_print_count = 0
                    #t_packet_received = 0
                    #t_packet_sent = 0
                    print("def | step {0} | action {1} | reward {2} | e {3}".format(step-1, def_past_action, defender_reward, e))
                    print("prio state was {0}".format(def_last_state))
                    print("this state was {0}".format(def_next_state))




                    # perform saves
                    if ep_num % 10000 == 0:
                        if self.defender_settings.save_model_mode in self.agentSaveModes:  # only save the first iteration 
                            agent.saveModel(self.file_path, ep_num, prefix)
                        if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                            self.adversarialMaster.saveModel(self.file_path, ep_num, prefix)

                
                # Note I've changed this to be a per episode thing
                if self.defender_settings.save_model_mode in self.agentSaveModes:
                    if ep_num < pre_train_episodes:
                        e = 1
                    elif e > self.defender_settings.startE:
                        e = self.defender_settings.startE
                    elif e > self.defender_settings.endE:
                        e -= step_drop 
                    elif e < self.defender_settings.endE:
                        #assert(1==3)
                        e = self.defender_settings.endE
                else:
                    e = self.defender_settings.endE
                



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




                
                

                #(legit_served, legit_sent, legal_per, illegal_served, illegal_sent) = net.getStepPacketStatistics()
                (legit_served_ep, legit_sent_ep, legit_per, illegal_served_ep, illegal_sent_ep) = net.getEpisodeStatisitcs()
                packet_served_lines.append("{0},{1},{2},{3},{4},{5}\n".format(ep_num, legit_served_ep, legit_sent_ep, legit_per, illegal_served_ep, illegal_sent_ep))
                reward_lines.append("{0},{1},{2},{3},{4},{5},{6}\n".format(ep_num, rList[-1], defender_reward, second, e, advRList[-1], adversary_reward))
                if len(loss) > 0:
                    last_loss = loss[-1]
                else:
                    last_loss = 0
                loss_lines.append("{0},{1},{2},{3}\n".format(ep_num,last_loss, e, ep_def_loss))
                if self.opposition_settings.is_intelligent and len(adv_loss)>0:
                    last_adv_loss = adv_loss[-1]
                    adv_loss_lines.append("{0},{1},{2},{3}\n".format(ep_num,last_adv_loss, e, ep_adv_loss))
            if self.defender_settings.save_model_mode in self.agentSaveModes: # only save the first iteration 
                # save the model only every 10,000 steps
                agent.saveModel(self.file_path, ep_num, prefix)

            if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                self.adversarialMaster.saveModel(self.file_path, ep_num, prefix)

        run_mode = self.defender_settings.save_model_mode.name

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



        print("{0} is:".format(self.defender_settings.name))



    def can_attack(self, current_second):

        if self.delay_attacks:
            if current_second<utility.ATTACK_START:
                return False
            if current_second>=(120- utility.ATTACK_START):
                # sort of cheating with putting the 120 right there
                return False
        return True



# def can_attack(self, current_second):
#     if self.delay_attacks in [attack_delay_mode.delay_start, delay_both_sides] and current_second<utility.ATTACK_START:
#         return False
#     elif self.delay_attacks == attack_delay_mode.delay_both_sides and current_second >

    

 

