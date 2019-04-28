"""
Idea is to run AIM with the assumption it's working and 
try to get results kinda close to Malialis

Parameters to tune:
delta. 0.05 increments from 0.1 to 0.4 - 8
beta: 1.25 / 1.5 / 2 / 2.5  - 3
Ls: Margin inbetween - 5 / 10 / 15/ 20 / 25/ 30 / 40 % - 7


8 * 3 * 7 ~ 2.4 hours for each grid search
"""
import sys
import experiment
import network.hosts as hostClass
import network.network_new
from mapsAndSettings import *
import numpy as np
import runAttacks


# class AIMDtest(object):
#     name = "AIMD"
#     group_size = 1
#     delta = 0.3 # additive increase
#     beta = 2 # multiplicative decrease
#     epsilon = 0.1 # our error

#     stateRepresentation = stateRepresentationEnum.only_server # WRONG
#     sub_agent = agent.AIMD.AIMDagent
    

#     num_episodes = 1
#     max_epLength = 30
#     y = 0
#     tau = beta
#     update_freq = None
#     batch_size = None
#     pre_train_steps = delta
#     annealing_steps = 0
#     startE = 0
#     endE = 0
#     stepDrop = 0
#     reward_overload = None



adversarialLeaf = hostClass.adversarialLeaf

opposition = adv_constant


###
# Settings
assignedNetwork =  NetworkMalialisSmall #NetworkSingleTeamMalialisMedium
assignedAgent =  AIMDsettings #ddqnSingleNoCommunicate #ddqn100MediumHierarchical
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
parameter_tune = True
assignedAgent.encoders = None

assignedAgent.save_model_mode = defender_mode_enum.save
trainHost = adv_constant 



network_emulator = network.network_new.network_full #network_quick # network_full

###


assignedNetwork.emulator = network_emulator


twist="{0}".format(network_emulator.name)
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation)
file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, trainHost)


"""
Variables:
epsilon
beta (second, do 2 first though)
bucketValue (do as percentage of maximum of server)
delta (bottom)


"""
# epsilon_values = np.arange(0.001, 0.05, 0.01).tolist()
# epsilon = 0.0001
beta_values = np.arange(1.25, 4, 0.25).tolist()
beta_values.remove(2)
beta_values.insert(0,2)
buck_values = np.arange(0.0, 2, 0.5).tolist()
delta_values = np.arange(0.05, 0.5, 0.05).tolist()

repeats = len(delta_values) * len(beta_values) * len(buck_values)
print("repeats = {0}".format(repeats))
print(len(delta_values))
print(len(beta_values))
print(len(buck_values))
# print(len(epsilon_values))


steps_per_second = 25

if parameter_tune:
    i = 0

    for beta in beta_values:
        for buck_value in buck_values:
            for delta in delta_values:
                assignedAgent.buck_value = buck_value
                print("testing for {0} {1} {2}".format(delta, beta, buck_value))
                assignedNetwork.bucket_capacity = assignedNetwork.upper_boundary*buck_value
                print("bucket is = {0}".format(assignedNetwork.bucket_capacity))
                assignedAgent.delta = delta
                assignedAgent.beta = beta
                #assignedAgent.epsilon = epsilon
                runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, opposition, i, steps_per_second)
                i+=1

    merge_summaries(file_path, i)
else:
    #experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="{2}{0}Alias{1}".format(numTiles, partition, network_emulator.name))

    experiment = experiment.Experiment(trainHost, assignedNetwork, assignedAgent, opposition)

    genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
    runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, opposition, 0)
