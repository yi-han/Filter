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


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack

adversarialLeaf = hostClass.adversarialLeaf


###
# Settings NetworkMalialisSmall
assignedNetwork =   NetworkSingleTeamMalialisMedium
assignedAgent =  AimdJeremy #ddqnSingleNoCommunicate #ddqn100MediumHierarchical
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
loadAttacks = False
assignedAgent.encoders = None

# print("\n\nSETTING TO JEREMY MODE\n\n\n")
# assignedNetwork.functionPastCapacity = False

assignedAgent.save_model_mode = defender_mode_enum.load
trainHost = adversarialLeaf #coordAttack # conAttack #driftAttack #adversarialLeaf

opposition = adv_constant #adv_random #adv_constant
intelligentOpposition = ddAimdAltLoads #ddAdvAntiAimd #DdCoordinatedLowlongDlowSettings #DdCoordinatedMasterSettings #DdRandomMasterSettings
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




network_emulator = network.network_new.network_full #network_quick # network_full

###


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

