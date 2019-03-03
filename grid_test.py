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
import agent.ddqnCentralised as ddCen
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


conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease
# driftAttack = hostClass.DriftAttack
coordAttack = hostClass.CoordinatedRandom
adversarialLeaf = hostClass.adversarialLeaf



attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 

###
# Settings
assignedNetwork =  NetworkMalialisSmall #NetworkSingleTeamMalialisMedium
assignedAgent =  AIMDsettings #ddqnSingleNoCommunicate #ddqn100MediumHierarchical
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
parameter_tune = True
assignedAgent.encoders = None

assignedAgent.save_model_mode = defender_mode_enum.save
trainHost = conAttack #coordAttack # conAttack #driftAttack #adversarialLeaf
assignedNetwork.drift = 0

# intelligentOpposition = DdRandomMasterSettings #DdCoordinatedLowlongDlowSettings #DdCoordinatedMasterSettings #DdRandomMasterSettings
# intelligentOpposition.save_model_mode = defender_mode_enum.save
intelligentOpposition = None


network_emulator = network.network_new.network_full #network_quick # network_full

###


assignedAgent.trained_drift = assignedNetwork.drift # we use this a copy of what the trained drift value is. We dont use this for the experiment
assignedNetwork.emulator = network_emulator


twist="{0}".format(network_emulator.name)
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation)
file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, trainHost)

if assignedAgent.save_model_mode is defender_mode_enum.load and intelligentOpposition \
    and intelligentOpposition.save_model_mode is defender_mode_enum.save:
    # we've set the filepath, now we need to ensure that we have the right adversary
    assert(trainHost==conAttack)
    trainHost = adversarialLeaf
"""
Variables:
epsilon
beta (second, do 2 first though)
bucketValue (do as percentage of maximum of server)
delta (bottom)


"""
epsilon_values = np.arange(0.001, 0.05, 0.01).tolist()
beta_values = np.arange(1.25, 4, 0.25).tolist()
beta_values.remove(2)
beta_values.insert(0,2)
buck_values = np.arange(0.1, 1, 0.1).tolist()
delta_values = np.arange(0.05, 1.5, 0.1).tolist()

repeats = len(delta_values) * len(beta_values) * len(buck_values) * len(epsilon_values)
print("repeats = {0}".format(repeats))
print(len(delta_values))
print(len(beta_values))
print(len(buck_values))
print(len(epsilon_values))


iterations_per_action = 35

if parameter_tune:
    i = 0

    for epsilon in epsilon_values:
        for beta in beta_values:
            for buck_value in buck_values:
                for delta in delta_values:
                    assignedAgent.buck_value = buck_value
                    print("testing for {0} {1} {2} {3}".format(delta, beta, buck_value, epsilon))
                    assignedNetwork.bucket_capacity = assignedNetwork.upper_boundary*buck_value
                    print("bucket is = {0}".format(assignedNetwork.bucket_capacity))
                    assignedAgent.delta = delta
                    assignedAgent.beta = beta
                    assignedAgent.epsilon = epsilon
                    runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition, i, iterations_per_action)
                    i+=1

    merge_summaries(file_path, i)
else:
    #experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="{2}{0}Alias{1}".format(numTiles, partition, network_emulator.name))

    experiment = experiment.Experiment(trainHost, assignedNetwork, assignedAgent, intelligentOpposition)

    genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
    runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition, 0)
