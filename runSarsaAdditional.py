import sys
import experiment
import network.hosts as hostClass
import network.network_new
import agent.tileCoding as tileCoding
import agent.sarsaCentralised as sarCen
import agent.linearSarsaCentralised as linCen
import agent.randomAgent as ranAg
#import agent.sarsaDecentralised as sarDec# import agent.ddqnDecentralised as ddDec
from mapsAndSettings import *
import runAttacks
assert(len(sys.argv)>=3)





class LinearSarsaSingular(object):
    # note we have two dependencies
    name = "LinearSarsaSingular"
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.0125
    update_freq = None
    batch_size = None
    num_episodes = 62501#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.throttler  

class LinearSarsaLong(LinearSarsaSingular):
    name = "LinearSarsaLong"
    num_episodes = 200001

class LinearSarsaNoOverloadLong(LinearSarsaSingular):
    name = "LinearNoOverloadLong"
    num_episodes = 100001
    reward_overload = None

class LinearSarsaNoOverload(LinearSarsaSingular):
    name = "LinearSarsaSingularNoOverload"
    reward_overload = None



class LinearSarsaSingularDDQNCopy(object):
    # copy from ddqnSingleNoCommunicate
    name = "LinearSarsaSingularDDQNCopy"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.01 #Rate to update target network toward primary network. 
    update_freq = None #How often to perform a training step.
    batch_size = None #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 20000 * max_epLength #40000 * max_epLength #
    annealing_steps = 60000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = linCen.Agent
    stateRepresentation = stateRepresentationEnum.throttler
    reward_overload = None
    group_size = 1 # number of filters each agent controls

class LinearSarsaLAI(object):
    name = "LinearSarsaLAI"
    max_epLength = 500
    y = 0
    tau = 0.001
    update_freq = None
    batch_size = None
    num_episodes = 100001#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 80000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    startE = 0.3 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate  

class LinearSarsaLAIreduced(LinearSarsaLAI):
    # same concept as the DDQN, lower learning rate ~ better results?
    name = "LinearSarsaLAIreduced"
    tau = 0.001

class LinearSarsaLAIshort(LinearSarsaLAI):
    name = "LinearLAIshort"
    max_epLength = 30
    annealing_steps = 80000 * max_epLength #1000*max_epLength #60000 * max_epLength 

class LinearLAIshortReduced(LinearSarsaLAIshort):
    name = "LAIshortAndReduced"
    tau = 0.003


class LinearSarsaLAIDDQN200(LinearSarsaLAI):
    # Idea (without using a ridiculous number of epLength, set the learning rate even lower and give proper exploration)
    name = "LinearDDQN200"
    max_epLength = 30
    tau = 0.001
    num_episodes = 200001 #200001#    
    pre_train_steps = 40000 * max_epLength #40000 * max_epLength #
    annealing_steps = 120000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    reward_overload = None  

class LinSarDDQN200HighTau(LinearSarsaLAIDDQN200):
    name = "LinearDDQN200HighTau"
    tau = 0.005

class LinLaiOverload(LinearSarsaLAIDDQN200):
    name = "LinLaiOverload"
    reward_overload = -1


class LinearSarsaLAIDDQN100Short(LinearSarsaLAI):
    # Idea (without using a ridiculous number of epLength, set the learning rate even lower and give proper exploration)
    name = "LinearDDQN100Short"
    max_epLength = 30
    tau = 0.001
    num_episodes = 100001 #200001#    
    pre_train_steps = 2000 * max_epLength #40000 * max_epLength #
    annealing_steps = 78000 * max_epLength  #120000 * max_epLength  #
    startE = 0.3
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps  
    reward_overload = None

class LinearLaiManyEpisodes(object):
    name = "LinearLaiManyEpisodes"
    max_epLength = 60
    y = 0
    tau = 0.001
    update_freq = None
    batch_size = None
    num_episodes = 1000001#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 800000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    startE = 0.3 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = None
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate  


class LinearTeamCommunicate(object):
    # communication up till the server
    name = "LinearTeamCommunicate"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = None #How often to perform a training step.
    batch_size = None #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 40000 * max_epLength #40000 * max_epLength #
    annealing_steps = 120000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = linCen.Agent
    stateRepresentation = stateRepresentationEnum.server
    reward_overload = -1
    group_size = 1 # number of filters each agent controls



class RandomAgent(object):
    name = "RandomLong"
    max_epLength = 500 # or 60 if test
    y = 0
    tau = 0.05
    update_freq = None
    batch_size = None
    num_episodes = 100001#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 80000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    startE = 0.3 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ranAg.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate      



# class GeneralSettings(object):
#     # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
#     debug = False
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

"""
Settings to change


"""
assignedNetwork = NetworkSingleTeamMalialisMedium
assignedAgent = LinearSarsaSingular
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
network_emulator = network.network_new.network_full # network_quick # network_full
loadAttacks = False



assignedAgent.save_model_mode = defender_mode_enum.save
trainHost = conAttack #coordAttack # conAttack #driftAttack #adversarialLeaf
assignedNetwork.drift = 25

intelligentOpposition = DdCoordinatedMasterSettings #DdRandomMasterSettings
intelligentOpposition.save_model_mode = defender_mode_enum.save
intelligentOpposition = None

###

assignedNetwork.emulator = network_emulator

if assignedAgent.save_model_mode is defender_mode_enum.load and intelligentOpposition \
    and intelligentOpposition.save_model_mode is defender_mode_enum.save:
    # we've set the filepath, now we need to ensure that we have the right adversary
    assert(trainHost==conAttack)
    trainHost = adversarialLeaf



attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 

if len(sys.argv)==4:
    partition = sys.argv[3]
else:
    partition = ""



assignedAgent.trained_drift = assignedNetwork.drift # we use this a copy of what the trained drift value is. We dont use this for the experiment


"""
This is the encoder for the sarsa, this might be better positioned somewhere else
"""
encoders = []
level = 0 # level 0 is throttlers, level 1 is intermeditary etc
for max_hosts in assignedNetwork.max_hosts_per_level:
    maxThrottlerBandwidth = assignedNetwork.rate_attack_high * max_hosts # a throttler doesn't face more than X
    if level == 0:
        numTiles = 6 * max_hosts
    elif assignedAgent.stateRepresentation == stateRepresentationEnum.throttler:
        continue
    else:
        numTiles = 6 # just set at 6.
    numTilings = 8
    tileCoder = tileCoding.myTileInterface(maxThrottlerBandwidth, numTiles, numTilings)
    encoders.append(tileCoder)
    level += 1
assignedAgent.encoders = encoders


twist = "{2}{0}Alias{1}".format(numTiles, partition, network_emulator.name)
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation)

if (len(sys.argv)==4) and sys.argv[3] != "" :
    file_path = sys.argv[3]
    proper_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, trainHost)

    print("file should be: {0}".format(proper_path))
else:
    file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, trainHost)

print('the filepath is {0}'.format(file_path))


if loadAttacks:
    runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition)

else:
    #experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="{2}{0}Alias{1}".format(numTiles, partition, network_emulator.name))

    experiment = experiment.Experiment(trainHost, assignedNetwork, assignedAgent, intelligentOpposition)

    start_num = int(sys.argv[1])
    length_core= int(sys.argv[2])

    for i in range(length_core):
        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        # genericAgent = None        
        print("Im doing it for {0}".format(start_num+i))
        experiment.run(start_num+i, genericAgent, file_path)

    if start_num==0:
        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition)


"""

for attackClass in attackClasses:
    sarsaGeneric = create_generic_dec(assignedAgent, assignedNetwork)
    # sarsaGeneric = None
    
    attack_location = load_attack_path+attackClass.getName()+".apkl"

    exp = experiment.Experiment(attackClass, assignedNetwork, 
        assignedAgent, twist= "NoPTTile1Save", load_attack_path=attack_location)
    exp.run(0, sarsaGeneric)
"""

"""


exp = experiment.Experiment(conAttack, assignedNetwork, 
    assignedAgent, load_attack_path=None)


start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

for i in range(length_core):
    sarsaGeneric = create_generic_dec(assignedAgent, assignedNetwork)
    print("Im doing it for {0}".format(start_num+i))
    exp.run(start_num+i, sarsaGeneric)
    # exp.run(start_num+i)

"""



