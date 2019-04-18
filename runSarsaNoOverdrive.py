import sys
import experiment
import network.hosts as hostClass
import network.network_new
import agent.tileCoding as tileCoding
import agent.linearSarsaCentralised as linCen
import agent.randomAgent as ranAg
from mapsAndSettings import *
import runAttacks
assert(len(sys.argv)>=3)




class LinearSarsaSingular(object):
    # note we have two dependencies
    name = "LinearSarsaSingular"
    discount_factor = 0
    tau = 0.1
    update_freq = 4
    batch_size = None
    num_episodes = 62500#62500
    pre_train_episodes = 0#2000
    annealing_episodes = 50000
    startE = 0.4 #0.4
    endE = 0.0
    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    history_size = 1 # number of past iterations to look at
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.throttler  
    has_bucket = False
    actions_per_second = 0.5 # make an decision every 2 seconds
    
class LinSingularExploration(LinearSarsaSingular):
    name = "linSingExp"
    endE = 0.1

class LinearSliding(LinearSarsaSingular):
    name = "SlidingMal"
    actions_per_second = 2
    # num_episodes = 200000

class LinearSarsaSingularDDQNCopy(object):
    # copy from ddqnSingleNoCommunicate
    name = "LinearSarsaSingularDDQNCopy"
    discount_factor = 0    
    tau = 0.01 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = None #How many experiences to use for each training step.
    num_episodes = 200001 #200001#    
    pre_train_episodes = 20000 #40000 #
    annealing_episodes = 60000  #120000  #
    startE = 1
    endE = 0.0
    history_size = 1 # number of past iterations to look at
    agent = None
    sub_agent = linCen.Agent
    stateRepresentation = stateRepresentationEnum.throttler
    reward_overload = None
    group_size = 1 # number of filters each agent controls
    has_bucket = False
    actions_per_second = 0.5 # make an decision every 2 seconds

class LinSinDDMemory(LinearSarsaSingularDDQNCopy):
    name = "LinSinDDMemory"
    tau = 0.005
    history_size = 5

class LinearSarsaLAI(object):
    name = "LinearSarsaLAI"
    #max_epLength = 500
    discount_factor = 0
    tau = 0.01
    update_freq = 4
    batch_size = None
    num_episodes = 100001#82501
    pre_train_episodes = 0#2000 * max_epLength
    annealing_episodes = 80000 #10 #60000 
    startE = 0.3 #0.4
    endE = 0.0
    history_size = 1 # number of past iterations to look at

    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate  
    has_bucket = False



class LinearSarsaLAIDDQN350(LinearSarsaLAI):
    # Idea (without using a ridiculous number of epLength, set the learning rate even lower and give proper exploration)
    name = "LinearDDQN350"
    tau = 0.005
    num_episodes = 350001 #200001#    
    pre_train_episodes = 40000 #40000 #
    annealing_episodes = 160000  #120000  #
    startE = 1
    endE = 0.0
    episodeDrop = (startE - endE)/annealing_episodes
    reward_overload = None  
    actions_per_second = 0.5

class LinHierMemory(LinearSarsaLAIDDQN350):
    name = "LinHierMemory"
    tau = 0.001
    history_size = 5

class LinTest(object):
    # note we have two dependencies
    name = "LinearTest"
    discount_factor = 0
    tau = 0.1
    update_freq = 4
    batch_size = None
    num_episodes = 20#82501
    pre_train_episodes = 1#2000
    annealing_episodes = 5 #10 #60000 
    startE = 0.4 #0.4
    endE = 0.0
    history_size = 1 # number of past iterations to look at
    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.throttler  
    has_bucket = False
    actions_per_second = 0.5

# The class of the adversary to implement
conAttack = hostClass.ConstantAttack

adversarialLeaf = hostClass.adversarialLeaf


"""
Settings to change
"""

assignedNetwork = NetworkSixFour
assignedAgent = LinearSarsaLAIDDQN350
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
network_emulator = network.network_new.network_full # network_quick # network_full
loadAttacks = True



# print("\n\nSETTING TO JEREMY MODE\n\n\n")
# assignedNetwork.functionPastCapacity = False


assignedAgent.save_model_mode = defender_mode_enum.load
trainHost = adversarialLeaf #coordAttack # conAttack #driftAttack #adversarialLeaf
assignedNetwork.drift = 0

opposition = adv_constant #adv_random # adv_constant
intelligentOpposition =  DdGenericSplitShort #
intelligentOpposition.save_model_mode = defender_mode_enum.save
# intelligentOpposition = None


assert(trainHost==adversarialLeaf)
assert(opposition.is_intelligent==False) # not meant to be a smart advesary
if intelligentOpposition == None:
    print("no smart opposition detected")
    intelligentOpposition = opposition
    intelligentOpposition.save_model_mode = defender_mode_enum.neither
else:
    assert(assignedAgent.save_model_mode != defender_mode_enum.save)






###
assignedAgent.trained_drift = assignedNetwork.drift # we use this a copy of what the trained drift value is. We dont use this for the experiment
assignedNetwork.emulator = network_emulator
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation)

"""
This is the encoder for the sarsa, this might be better positioned somewhere else
"""
encoders = []
level = 0 # level 0 is throttlers, level 1 is intermeditary etc
for max_hosts in assignedNetwork.max_hosts_per_level:
    maxThrottlerBandwidth = 2 * assignedNetwork.rate_attack_high * max_hosts # a throttler doesn't face more than X
    if level == 0:
        numTiles = 6 * max_hosts
    elif assignedAgent.stateRepresentation == stateRepresentationEnum.throttler:
        continue
    else:
        numTiles = 6 # just set at 6.
    numTilings = 8
    tileCoder = tileCoding.myTileInterface(maxThrottlerBandwidth, numTiles, numTilings)
    encoders.extend([tileCoder]*assignedAgent.history_size)
    level += 1
assignedAgent.encoders = encoders

twist = "{0}{1}".format(numTiles, network_emulator.name) #{2}{0}Alias{1}".format(numTiles, "", network_emulator.name)


if (len(sys.argv)==4) and sys.argv[3] != "" :
    file_path = sys.argv[3]
    proper_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, opposition)
    print("file should be: {0}".format(proper_path))
else:
    file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, twist, opposition)

print('the filepath is {0}'.format(file_path))

# if assignedAgent.save_model_mode is defender_mode_enum.load and intelligentOpposition \
#     and intelligentOpposition.save_model_mode is defender_mode_enum.save:
#     # we've set the filepath, now we need to ensure that we have the right adversary
#     assert(trainHost==conAttack)
#     trainHost = adversarialLeaf
#if intelligentOpposition.save_model_mode is defender_mode_enum.neither:

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




