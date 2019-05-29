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
    reward_function = AGENT_REWARD_ENUM.overload
    stateRepresentation = stateRepresentationEnum.throttler  
    has_bucket = False
    actions_per_second = 0.5 # make an decision every 2 seconds
    

class LinOrigLengthened(LinearSarsaSingular):
    name = "linOrigLengthened"
    tau = 0.01 #Rate to update target network toward primary network. 
    num_episodes = 120000 #200001#    
    pre_train_episodes = 20000 #40000 #
    annealing_episodes = 60000  #120000  #

class LinLengthenedSliding(LinOrigLengthened):
    name = "LinLengthenedSliding"
    actions_per_second = 2

class LinNegative(LinOrigLengthened):
    # copy from ddqnSingleNoCommunicate
    name = "LinearSarsaNegative"
    sub_agent = linCen.Agent
    stateRepresentation = stateRepresentationEnum.throttler
    reward_function = AGENT_REWARD_ENUM.sliding_negative




class LinSinPackets(LinOrigLengthened):
    name = "LinSinPackets"
    reward_function = AGENT_REWARD_ENUM.packet_logic

class linSinPacketsSliding(LinSinPackets):
    name = "linSinPacketsSliding"
    actions_per_second = 2

# class LinSinDDMemory(LinearSarsaSingularDDQNCopy):
#     name = "LinSinDDMemory"
#     tau = 0.005
#     history_size = 5

class linMarlFH(object):
    name = "linMarlFH"
    #max_epLength = 500
    discount_factor = 0
    tau = 0.005
    update_freq = 4
    batch_size = None
    num_episodes = 350000#82501
    pre_train_episodes = 20000
    annealing_episodes = 60000 
    startE = 1 #0.4
    endE = 0.0
    history_size = 1 # number of past iterations to look at

    agent = None
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    #stateRepresentation = stateRepresentationEnum.leaderAndIntermediate  
    has_bucket = False
    actions_per_second = 0.5
    reward_function = AGENT_REWARD_ENUM.packet_logic
    stateRepresentation = stateRepresentationEnum.up_to_server

class linHierOrigReward(linMarlFH):
    name = "linHierOrigReward"
    reward_function = AGENT_REWARD_ENUM.overload


# class LinearSarsaLAIDDQN350(LinearSarsaLAI):
#     # Idea (without using a ridiculous number of epLength, set the learning rate even lower and give proper exploration)
#     name = "LinearDDQN350"
#     tau = 0.005
#     num_episodes = 350001 #200001#    
#     pre_train_episodes = 40000 #40000 #
#     annealing_episodes = 160000  #120000  #
#     startE = 1
#     endE = 0.0
#     episodeDrop = (startE - endE)/annealing_episodes
#     reward_function = AGENT_REWARD_ENUM.sliding_negative
#     actions_per_second = 0.5
#     stateRepresentation = stateRepresentationEnum.up_to_server



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
    stateRepresentation = stateRepresentationEnum.throttler  
    has_bucket = False
    actions_per_second = 0.5



# The class of the adversary to implement
conAttack = hostClass.ConstantAttack

adversarialLeaf = hostClass.adversarialLeaf


"""
Settings to change
"""

assignedNetwork = NetworkNineTwo
assignedAgent = LinearSarsaSingular
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
network_emulator = network.network_new.network_full # network_quick # network_full
loadAttacks = False



# print("\n\nSETTING TO JEREMY MODE\n\n\n")
# assignedNetwork.functionPastCapacity = False



assignedAgent.save_model_mode = defender_mode_enum.load
trainHost = adversarialLeaf #coordAttack # conAttack #driftAttack #adversarialLeaf

opposition = adv_constant #adv_random # adv_constant
intelligentOpposition =  DdGenericFinal #
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




