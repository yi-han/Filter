import sys
import experiment
import network.hosts as hostClass
import agent.ddqnCentralised as ddCen
import network.network_new
from mapsAndSettings import *

#import generic_run

import runAttacks


import agent.ddqnCentralised as ddCen
# import agent.ddqnDecentralised as ddDec

from mapsAndSettings import *
assert(len(sys.argv)>= 3)

class ddqnSingleNoCommunicate(object):
    group_size = 1
    name = "DDQN100SingleNoCommunicate"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.01 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 20000 * max_epLength #40000 * max_epLength #
    annealing_steps = 60000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.throttler
    reward_overload = None

class ddqnSingleSarsaCopy(object):
    # apart from 2000 pretrain and overload this is as close as it gets
    name = "DDQNDecGenMalialisAttempt" #used to be DDQNDecGenMalialisNoOpt
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = 4
    batch_size = 32
    num_episodes = 64501#82501
    pre_train_steps = 2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    group_size = 1 # number of filters each agent controls
    # stateletFunction = getStateletNoCommunication
    isCommunication = False
    reward_overload = None
    stateRepresentation = stateRepresentationEnum.throttler

class ddqnMalialisTrue(ddqnSingleSarsaCopy):
    # is the singleSarsaCopy but with reward overload
    name = "DDQNDecGenMalialisTrue"
    reward_overload = -1


class ddqnDoubleHierarchical(object):
    group_size = 1
    name = "DDQN200Hierarchical"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 200001 #200001#    
    pre_train_steps = 40000 * max_epLength #40000 * max_epLength #
    annealing_steps = 120000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate
    reward_overload = None    

class ddqnLAIlow(ddqnDoubleHierarchical):
    name = "ddqnLAIlowLearn"

    tau = 0.0005

class ddqnLAIhigh(ddqnDoubleHierarchical):
    name = "ddqnLAIhighLearn"

    tau = 0.005


class ddqn50MediumHierachical(object):
    group_size = 1
    name = "ddqn50MediumHierachical"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 50000 #200001#    
    pre_train_steps = 10000 * max_epLength #40000 * max_epLength #
    annealing_steps = 30000 * max_epLength  #120000 * max_epLength  #
    startE = 0.3
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate
    reward_overload = None       

class ddqn100MediumHierarchical(object):
    group_size = 1
    name = "ddqn100MediumHierarchical"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 20000 * max_epLength #40000 * max_epLength #
    annealing_steps = 60000 * max_epLength  #120000 * max_epLength  #
    startE = 0.3
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate
    reward_overload = None   

class ddqn100HierarchicalShort(object):
    # same as above but reduceing hte pre-train down by factor of 10
    group_size = 1
    name = "ddqn100Short"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 2000 * max_epLength #40000 * max_epLength #
    annealing_steps = 78000 * max_epLength  #120000 * max_epLength  #
    startE = 0.3
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate
    reward_overload = None       

class ddqn100HierarchicalOverload(ddqn100MediumHierarchical):
    name = "ddqn100Overload"
    reward_overload = -1

class ddqnServerCommunicate(object):
    group_size = 1
    name = "ddqn120ServerCommunicate"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 120001 #200001#    
    pre_train_steps = 20000 * max_epLength #40000 * max_epLength #
    annealing_steps = 80000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.server
    reward_overload = None  

# class GeneralSettings(object):
#     # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
#     #test = False # handled by saveModel
#     debug = False
#     #load_model = False
#     # save_attack = SaveAttackEnum.neither
#     tileFunction = None
    


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease
# driftAttack = hostClass.DriftAttack
coordAttack = hostClass.CoordinatedRandomNotGradual
adversarialLeaf = hostClass.adversarialLeaf



attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 

###
# Settings
assignedNetwork =  NetworkMalialisSmall #NetworkSingleTeamMalialisMedium
assignedAgent = ddqnSingleNoCommunicate #ddqn100MediumHierarchical
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
loadAttacks = True
assignedAgent.encoders = None

assignedAgent.save_model_mode = defender_mode_enum.load
trainHost = conAttack #coordAttack # conAttack #driftAttack #adversarialLeaf
assignedNetwork.drift = 0


# DdRandomMasterSettings = None
DdRandomMasterSettings.save_model_mode = defender_mode_enum.save

network_emulator = network.network_new.network_full #network_quick # network_full

###


assignedAgent.trained_drift = assignedNetwork.drift # we use this a copy of what the trained drift value is. We dont use this for the experiment
assignedNetwork.emulator = network_emulator

twist="{0}".format(network_emulator.name)
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation)
file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, trainHost)

if assignedAgent.save_model_mode is defender_mode_enum.load and DdRandomMasterSettings \
    and DdRandomMasterSettings.save_model_mode is defender_mode_enum.save:
    # we've set the filepath, now we need to ensure that we have the right adversary
    assert(trainHost==conAttack)
    trainHost = adversarialLeaf

if loadAttacks:
    runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, DdRandomMasterSettings)



else:
    #experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="{2}{0}Alias{1}".format(numTiles, partition, network_emulator.name))

    experiment = experiment.Experiment(trainHost, assignedNetwork, assignedAgent, DdRandomMasterSettings)

    start_num = int(sys.argv[1])
    length_core= int(sys.argv[2])

    for i in range(length_core):
        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        # genericAgent = None        
        print("Im doing it for {0}".format(start_num+i))
        experiment.run(start_num+i, genericAgent, file_path)

    if start_num==0:
        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, DdRandomMasterSettings)



"""
if loadAttacks:
    for attackClass in attackClasses:
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        # genericAgent = None
        attack_location = load_attack_path+attackClass.getName()+".apkl"

        exp = experiment.Experiment(attackClass, GeneralSettings, assignedNetwork, 
            assignedAgent, twist="{0}".format(network_emulator.name), load_attack_path=attack_location)
        exp.run(0, genericAgent)

    getSummary(attackClasses, exp.load_path, assignedAgent)
else:
    experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="{0}".format(network_emulator.name))
    # experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, "double")


    start_num = int(sys.argv[1])
    length_core= int(sys.argv[2])

    for i in range(length_core):
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        # genericAgent = None        
        print("Im doing it for {0}".format(start_num+i))
        experiment.run(start_num+i, genericAgent)
"""

