"""

Input: Network, defender, path, attacker

Runs simulation, sends state to learning agent, gets response, sends response to network.
Is compatible with both a learning defender and a learning attacker (only one should learn at a time)




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
16) SaveModelEnum being caleled load_model_enum???
17) Don't thing generic update (actionTo...) is compatible with differnt size agents
18) Investigate why is actionReplay only activating after pretraining???
"""

from __future__ import division

import numpy as np
import os
from enum import Enum
import network.hosts as hosts
import network.utility as utility
import mapsAndSettings
import errno


def calculate_e(current_episode, pretraining_episodes, startE, endE, annealing_episodes):
    # initiate the exploration coefficient.
    # 1 means exploration of new strategies, 0 means exploitation of learnt strategies
    if current_episode < pretraining_episodes:
        return 1
    elif current_episode >= (pretraining_episodes + annealing_episodes):
        return endE
    elif current_episode == pretraining_episodes:
        return startE
    else:
        percentRemaining = 1 - ((current_episode- pretraining_episodes)/annealing_episodes)
        assert(percentRemaining > 0 and percentRemaining < 1)
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
        print(NetworkClass.N_state)
        print(NetworkClass.action_per_throttler**NetworkClass.N_state)

        self.opposition_settings = oppositionSettings


        self.agentLoadModes = [mapsAndSettings.defender_mode_enum.test_short, mapsAndSettings.defender_mode_enum.load, mapsAndSettings.defender_mode_enum.load_save, mapsAndSettings.defender_mode_enum.load_continue]
        self.agentSaveModes = [mapsAndSettings.defender_mode_enum.save, mapsAndSettings.defender_mode_enum.load_save, mapsAndSettings.defender_mode_enum.load_continue]
        self.agentInitialiseMode = [mapsAndSettings.defender_mode_enum.save, mapsAndSettings.defender_mode_enum.load_continue]
        self.agentTestModes = [mapsAndSettings.defender_mode_enum.test_short]


    def run(self, prefix, agent, file_path):
        N_state = self.network_settings.N_state # number of states for defender
        action_per_throttler = self.network_settings.action_per_throttler # number of actions for defender
        self.file_path = file_path
        update_freq = self.defender_settings.update_freq 
        batch_size = self.defender_settings.batch_size
        #create lists to contain total rewards and steps per episode
        rList = [] # reward per episode for defender
        advRList = [] # reward per episode for attacker
        loss = [] # learning loss for defender (if reinforcement learning)
        adv_loss = [] # learning loss for attacker ( if reinforcement Learning)
        

        # Following files are used for recording actions and rewards of defender and attacker. Exported to CSV
        # determine reward for a prediction at start of episode, we choose the second step as first step is random
        reward_lines = []
        loss_lines = []
        adv_loss_lines = []
        packet_served_lines = []    
        server_actions_lines = [] # file for recording the actions and the moves by actors
        fail = 0 # The total number of fails 
        e = 1 # always start full exploration. Gets overwritten in training
        
        # During evaluation and training of attacker, the attacker starts a few seconds after simulation starts
        self.delay_attacks = False 

        """
        Determine the episodes and exploration for the defender

        """

        if self.defender_settings.save_model_mode in self.agentTestModes:
            # evaluation
            num_episodes = 500
            ep_length = self.network_settings.ep_length*2 # during evaluation simulations are twice as long as training
            self.delay_attacks = True # 
        else:
            #training
            num_episodes = self.defender_settings.num_episodes
            ep_length = self.network_settings.ep_length

        # code for determining the rate exploration drops after each episode 
        if self.defender_settings.save_model_mode in self.agentInitialiseMode: 
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
            self.delay_attacks = True # align attacker training with evaluation
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
            # non-intelligent attackers dont require trianing
            self.adversarialMaster =  self.opposition_settings.adversary_class(self.opposition_settings, ep_length)
            adv_e = 0

        net = self.network_settings.emulator(self.network_settings, self.adversary_class, self.defender_settings, self.adversarialMaster, load_attack_path=self.load_attack_path)

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
        
        # initialise headers for exported CSVs

        reward_lines.append("Episode,TotalReward,LastReward,LengthEpisode,e,AdvTotalReward,AdvLastReward\n")
        packet_served_lines.append("Episode,LegalReceived,LegalSent,PercentageReceived,IllegalServed,IllegalSent\n")
        loss_lines.append("Episode,Loss,Exploration,EpDefLoss\n")
        #self.episode_rewards = []
        if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
            adv_loss_lines.append("Episode,Loss,Exploration,EpDefLoss\n")
        server_actions_line = "Episode,Second,LegalReceived,LegalSent,LegalPercentage,IllegalServed,IllegalSent,TotalServed,TotalSent,AssociatedReward,LegalCap,IllegalCap,TotalCap,NumAdvesary"


        ep_init = 0


        with agent:
            # exported CSV headers have different number of columns depending on number of learning agents
            for i in range(agent.num_agents):
                server_actions_line += ",DefAction{0}".format(i)
            for i in range(self.opposition_settings.num_adv_agents):
                server_actions_line += ",AdvAction{0}".format(i)
            server_actions_line += "\n"
            server_actions_lines.append(server_actions_line)

            # initiate the attacker
            self.adversarialMaster.__enter__()

            # determine initial episode (we might be loading a half completed version)
            if self.defender_settings.save_model_mode in self.agentLoadModes : #mapsAndSettings.defender_mode_enum.test
                episode = agent.loadModel(self.file_path, prefix)
                if self.defender_settings.save_model_mode == mapsAndSettings.defender_mode_enum.load_continue:
                    ep_init = max(episode, ep_init) # edge case: Return -1 if folder doesn't exist
                else:
                    print("returned an episode of {0}".format(episode))
                    assert(episode != -1) # used to flag doesnt exist
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
            
            adversary_reward = None

            adv_print_reward = 0
            adv_print_count = 0



            ### Initialisation complete, now run the simulation!

            print("\n\n Starting at episode {0}".format(ep_init))
            print("num_episodes {0} episode length {1} iterations between each second {2}".format(num_episodes, ep_length, self.network_settings.iterations_between_second))
            print("defender exploration = {0}".format(e))
            print("adversary exploration = {0}".format(adv_e))
            for ep_num in range(ep_init, num_episodes):
                # initialise the episode

                net.reset() # reset the network
                agent.reset_episode(net)
                ep_adv_loss = 0
                ep_def_loss = 0
                num_defender_moves = 0 # number defender moves this episode
                num_adversary_moves = 0                
                if self.opposition_settings:
                    self.adversarialMaster.initiate_episode(ep_num)

                rAll = 0 # accumulative defender reward for system in the episode.
                advRAll = 0 # total defenderreward for episode
                
                if self.network_settings.save_per_step_stats:
                    (legal_capacity, illegal_capacity, total_capacity) = net.getHostCapacity()


                adv_next_state = None
                adv_next_action = None
                
                def_next_state = None
                def_next_action = None
                # episode_steps = ep_length * self.network_settings.iterations_between_second
             
                step = -1

                # iterate through every second of episode length
                for second in range(ep_length):
                    for iteration in range(self.network_settings.iterations_between_second):
                        # each episode has X iterations per second (allows finite breakdown in ms)
                        step += 1

                        # attacker choooses move
                        if step % adversary_move == 0:
                            adv_step = step/adversary_move # the step for the adversary
                            
                            # update state
                            adv_past_state = adv_next_state
                            adv_past_action = adv_next_action
                            self.adversarialMaster.update_state(net)
                            adv_next_state = self.adversarialMaster.get_state()
                            # calculate action (considers exploration)
                            adv_next_action = self.adversarialMaster.predict(adv_next_state, adv_e, adv_step, self.can_attack(second)) # generate an action
                            num_adversary_moves += 1

                            # Reward attacker based on success of prior move 
                            if num_adversary_moves > 1:
                                adv_print_count += 1
                                if self.opposition_settings.is_intelligent: 
                                    adversary_reward = self.adversarialMaster.calculate_reward()
                                    advRAll += adversary_reward  
                                    if self.opposition_settings.save_model_mode in self.agentSaveModes:
                                        adversary_done = False
                                        if self.can_attack(second-1):    
                                            # save episode into action replay
                                            self.adversarialMaster.update(adv_past_state, adv_past_action, adv_next_state, adversary_done, adversary_reward, adv_next_action) # num_adversary_moves ?
                                            
                                            # every four steps the agent does a batch learn following experience replay
                                            if num_adversary_moves % self.opposition_settings.update_freq == 0:
                                                adv_l = self.adversarialMaster.actionReplay(adv_next_state, self.opposition_settings.batch_size)
                                                adv_loss.append(adv_l)
                                                ep_adv_loss += abs(adv_l)


                                    self.adversarialMaster.update_past_state(adv_next_action)




                        # defender chooses move
                        if step % defender_move == 0:

                            def_step = step/defender_move
                            
                            def_last_state = def_next_state
                            def_past_action = def_next_action

                            agent.update_state(net)
                            def_next_state = agent.get_state()
                            def_next_action = agent.predict(def_next_state, e) # generate an action
                            newDefAction = True
                            num_defender_moves += 1
                            

                            # reward defender based on success of last action
                            if num_defender_moves > 1:

                                """
                                We assume this is only for training.
                                We also assume that during training our reward is calculated over last 2 seconds
                                """

                                if self.defender_settings.save_model_mode in self.agentSaveModes:
                                    defender_reward = net.get_reward(self.defender_settings.reward_function)

                                    agent_done = False
                                    agent.update(def_last_state, def_past_action, def_next_state, agent_done, defender_reward, def_next_action)


                                    if num_defender_moves % update_freq == 0:
                                        l = agent.actionReplay(def_next_state, batch_size)
                                        if l:
                                            loss.append(l)
                                            ep_def_loss += abs(l)


    

                        # moves are fed into network simulation
                        net.simulate_traffic(def_next_action, adv_next_action, step, newDefAction)
                        newDefAction = False # set this as false if it's not a new action
                        def_current_action = def_next_action
                        adv_current_action = adv_next_action
                
                    
                    # At the end of a second record reward
 
                    if second % mapsAndSettings.SECONDS_STANDARD_INTERVAL == 0 and num_defender_moves>1:
                        defender_reward = net.get_reward(self.defender_settings.reward_function)

                        rAll += defender_reward
                        reward_print_count += 1
                    
                        #print("\n\n\nSecond {0} Move = {1} State = {2}".format(second, def_past_action, def_last_state))


                    """
                    At the end of every second we record the percentage of traffic that was serviced by the server 

                    """
                    # print("testing actions {0}".format(def_current_action))
                    (legit_served, legit_sent, legal_per, illegal_served, illegal_sent) = net.updateEpisodeStatistics(second)
                    self.adversarialMaster.update_reward(second, legit_served, legit_sent)

                    if self.network_settings.save_per_step_stats:
                        total_sent = legit_sent+illegal_sent

                        total_served = legit_served+illegal_served
                        reward_window = net.get_reward(self.defender_settings.reward_function)
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
                END OF THE EPISODE
                - Record statistics
                """

                # do one last reward for the last episode. 
                if self.defender_settings.save_model_mode in self.agentSaveModes:
                    agent_done = True
                    final_state = agent.get_state()
                    defender_reward = net.get_reward(self.defender_settings.reward_function)
                    empty_set = [None] * len(def_next_state) # a row of Nones for next state/action
                    agent.update(def_next_state, def_next_action, final_state, agent_done, defender_reward, empty_set) 

                if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                    assert(self.can_attack(second-1))
                    adversary_done = True
                    final_state = self.adversarialMaster.get_state()
                    adversary_reward = self.adversarialMaster.calculate_reward()
                    empty_set = [None] * len(adv_next_state)
                    self.adversarialMaster.update(adv_next_state, adv_next_action, final_state, adversary_done, adversary_reward, empty_set) # num_adversary_moves ?


                # end of an episode we record some statistics
                rList.append(rAll)
                advRList.append(advRAll)
                reward_per_print += rAll
                adv_print_reward += advRAll

                if ep_num % 1000 == 0:
                    print("\n\nCompleted Episode - {0}".format(ep_num))
                    print("average reward = {0}".format((reward_per_print/reward_print_count)*100))
                    print("adversary reward = {0}".format((adv_print_reward/adv_print_count)*100))
                    reward_per_print = 0
                    reward_print_count = 0

                    adv_print_reward = 0
                    adv_print_count = 0

                    print("def | step {0} | action {1} | reward {2} | e {3}".format(step-1, def_past_action, defender_reward, e))
                    print("prio state was {0}".format(def_last_state))
                    print("this state was {0}".format(def_next_state))
                    if self.opposition_settings.is_intelligent:
                        print("adv_state = {0}".format(adv_past_state))
                    print("adv_action = {0}, adv_e = {1}".format(adv_current_action, adv_e))




                    # save the learning models every 10,000 episodes
                    if ep_num % 10000 == 0:
                        if self.defender_settings.save_model_mode in self.agentSaveModes:  # only save the first iteration 
                            agent.saveModel(self.file_path, ep_num, prefix)
                        if self.opposition_settings.is_intelligent and self.opposition_settings.save_model_mode in self.agentSaveModes:
                            self.adversarialMaster.saveModel(self.file_path, ep_num, prefix)

                
                # Update the exploration coefficients
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




                
                # packet statistics

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
            


            """
            End of experiment. Save the learning agents one last time and export experiment statistics

            """

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
        # calculates if attacker is allowed to attack
        if self.delay_attacks:
            if current_second<utility.ATTACK_START:
                return False
            if current_second>=(120- utility.ATTACK_START):
                return False
        return True

