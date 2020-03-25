"""

Trains IDA against the FairThrottle defender then evaluates over 500 episodes

"""


import sys
import experiment
import network.hosts as hostClass
import agent.ddqnCentralised as ddCen
import network.network_new
from mapsAndSettings import *
import runAttacks
import agent.ddqnCentralised as ddCen

assert(len(sys.argv)>= 3)


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
adversarialLeaf = hostClass.adversarialLeaf


###

# arg1 takes map intake. Options are MalialisSmall, Medium, NineTwo

mapID = int(sys.argv[1])
assert(mapID in [0,1,2]);

allMaps = [NetworkMalialisSmall, NetworkSingleTeamMalialisMedium, NetworkNineTwo]


# assign network settings for simulation
assignedNetwork =   allMaps[mapID];
assignedAgent =  AimdJeremy # IDA file
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
loadAttacks = False # set to True if already trained
assignedAgent.encoders = None


assignedAgent.save_model_mode = defender_mode_enum.load
trainHost = adversarialLeaf # link to zombie class of the attacker (sends the packets)

opposition = adv_constant #adv_random #adv_constant
intelligentOpposition = ddAimdSingle 
intelligentOpposition.save_model_mode = defender_mode_enum.load_continue


network_emulator = network.network_new.network_full # where the simulation happens
assignedNetwork.emulator = network_emulator

###




fileSuffix="{0}".format(network_emulator.name)
commStrategy = calc_comm_strategy(assignedAgent.stateRepresentation) # defines provided information

if (len(sys.argv)>=4) and sys.argv[3] != "" :
    file_path = sys.argv[3]
    proper_path = getPathName(assignedNetwork, assignedAgent, commStrategy, fileSuffix, opposition)

    print("file should be: {0}".format(proper_path))
else:
    file_path = getPathName(assignedNetwork, assignedAgent, commStrategy, fileSuffix, opposition)

print('the filepath is {0}'.format(file_path))



repeats = int(sys.argv[2]) # number of repeats

if loadAttacks: # agent already trained
    for i in range(0, repeats):
        runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition, i)

else: # train then evaluation

    experiment = experiment.Experiment(trainHost, assignedNetwork, assignedAgent, intelligentOpposition)

    for i in range(0, repeats):
        # each repetition train a seperate IDA
        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)

        print("Im doing it for repetition {0}".format(i))
        
        # train IDA
        experiment.run(i, genericAgent, file_path)

        # load attacker for evaluation
        genericAgent = create_generic_dec(assignedAgent, assignedNetwork)
        # run evaluation
        runAttacks.run_attacks(assignedNetwork, assignedAgent, file_path, intelligentOpposition, i)

