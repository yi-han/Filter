import sys
import experiment
import network.hosts as hostClass

import agent.sarsaCentralised as sarCen
import agent.sarsaDecentralised as sarDec# import agent.ddqnDecentralised as ddDec
from mapsAndSettings import *
assert(len(sys.argv)==3)






# class SarsaDecGeneric(object):
#     max_epLength = 30 # or 60 if test
#     y = 0
#     tau = 0.1
#     update_freq = None
#     batch_size = None
#     num_episodes = 62501#82501
#     pre_train_steps = 0#2000 * max_epLength
#     annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 

#     startE = 0.4 #0.4
#     endE = 0.0
#     stepDrop = (startE - endE)/annealing_steps
#     agent = None
#     sub_agent = sarCen.Agent
#     group_size = 1 # number of filters each agent controls

class GeneralSettings(object):
    SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    SaveModelEnum = Enum('SaveModel', 'neither save load test')
    save_attack_path = "./attack.pkl" # note you shouldn't be repeating this
    #test = False # handled by saveModel
    debug = False
    #load_model = False
    save_attack = SaveAttackEnum.neither
    save_model = SaveModelEnum.neither




# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease


assignedNetwork = NetworkMalialisSmall
assignedAgent = SarsaDecMaliasNoPT

sarsaGeneric = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
# sarsaGeneric = None

# experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, "NoPTTile1")
experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, "NoPTTile1Save")


start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

for i in range(length_core):
    print("Im doing it for {0}".format(start_num+i))
    experiment.run(start_num+i, sarsaGeneric)






