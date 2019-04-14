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

#from mapsAndSettings import *
assert(len(sys.argv)>= 3)

class ddqnSingleNoCommunicate(object):
    group_size = 1
    name = "DDQN100SingleNoCommunicate"
    discount_factor = 0    
    tau = 0.01 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 200001 #100001#    
    pre_train_episodes = 20000  #40000  #
    annealing_episodes = 60000   #120000   #
    startE = 1
    endE = 0.0
    history_size = 1 # number of past iterations to look at
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.throttler
    reward_overload = None
    has_bucket = False
    actions_per_second = 0.5 # make an decision every 2 seconds

class ddqnSingleMemory(ddqnSingleNoCommunicate):
    name = "ddqnSingleMemory"
    history_size = 5


class ddqn100MediumHierarchical(object):
    group_size = 1
    name = "ddqn100MediumHierarchical"
    discount_factor = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 200001 #200001#    
    pre_train_episodes = 20000  #40000  #
    annealing_episodes = 60000   #120000   #
    startE = 0.3
    endE = 0.0
    history_size = 1 # number of past iterations to look at
    agent = None
    sub_agent = ddCen.Agent
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate
    reward_overload = None   
    has_bucket = False

    actions_per_second = 0.5 # make an decision every 2 seconds


class ddqnHierMemory(ddqn100MediumHierarchical):
    name = "ddqnHierMemory"
    history_size = 5


class ddqnHierExploration(ddqn100MediumHierarchical):
    name = "ddqnHierExp"
    endE = 0.1

class ddqnSingularExploration(ddqnSingleNoCommunicate):
    name = "ddqnSingExp"
    endE = 0.1

class ddTest(ddqnHierMemory):
    name = "ddTest"
    num_episodes = 1001
    pre_train_episodes = 2
    annealing_episodes = 4
# The class of the adversary to implement
conAttack = hostClass.ConstantAttack

adversarialLeaf = hostClass.adversarialLeaf


###
# Settings NetworkMalialisSmall
assignedNetwork =   NetworkSixHard
assignedAgent =  ddqn100MediumHierarchical #ddqnSingleNoCommunicate #ddqn100MediumHierarchical
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
loadAttacks = False
assignedAgent.encoders = None

assignedAgent.save_model_mode = defender_mode_enum.save
trainHost = adversarialLeaf #coordAttack # conAttack #driftAttack #adversarialLeaf
assignedNetwork.drift = 0

opposition = adv_constant #adv_random #adv_constant
intelligentOpposition = DdGenericSplit #ddAdvAntiAimd #DdCoordinatedLowlongDlowSettings #DdCoordinatedMasterSettings #DdRandomMasterSettings
intelligentOpposition.save_model_mode = defender_mode_enum.save
intelligentOpposition = None


assert(trainHost==adversarialLeaf)
assert(opposition.is_intelligent==False) # not meant to be a smart advesary
if intelligentOpposition == None:
    print("no smart opposition detected")
    intelligentOpposition = opposition
    intelligentOpposition.save_model_mode = defender_mode_enum.neither
else:
    assert(assignedAgent.save_model_mode != defender_mode_enum.save)




network_emulator = network.network_new.network_full #network_quick # network_full

###


assignedAgent.trained_drift = assignedNetwork.drift # we use this a copy of what the trained drift value is. We dont use this for the experiment
assignedNetwork.emulator = network_emulator


twist="{0}".format(network_emulator.name)
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation)

if (len(sys.argv)>=4) and sys.argv[3] != "" :
    file_path = sys.argv[3]
    proper_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, opposition)

    print("file should be: {0}".format(proper_path))
else:
    file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, opposition)

print('the filepath is {0}'.format(file_path))



start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

if loadAttacks:
    for i in range(start_num, start_num+length_core):
        runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition, i)

else:
    #experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="{2}{0}Alias{1}".format(numTiles, partition, network_emulator.name))

    experiment = experiment.Experiment(trainHost, assignedNetwork, assignedAgent, intelligentOpposition)

    for i in range(start_num, length_core+start_num):

        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        # genericAgent = None        
        print("Im doing it for {0}".format(i))
        experiment.run(i, genericAgent, file_path)

        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition, i)

