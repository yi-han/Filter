import sys
import experiment
import network.hosts as hostClass

import agent.sarsaCentralised as sarCen
#import agent.sarsaDecentralised as sarDec# import agent.ddqnDecentralised as ddDec
from mapsAndSettings import *
assert(len(sys.argv)==3)

class SarsaDoubleSingleCommunicate(object):
    group_size = 1
    name = "Sarsa200SingleFullCommunicate"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = None #How often to perform a training step.
    batch_size = None #How many experiences to use for each training step.
    num_episodes = 200001 #200001#    
    pre_train_steps = 40000 * max_epLength #40000 * max_epLength #
    annealing_steps = 120000 * max_epLength  #120000 * max_epLength  #
    
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = sarCen.Agent

    stateletFunction = getStateletWithCommunication
    isCommunication = True # flag to demonstrate communication  

class SarsaCenMaliasOne(object):
    name = "sarsaCen100"
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.01
    update_freq = None
    batch_size = None
    # num_episodes = 62501
    # pre_train_steps = 0 * max_epLength
    # annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    num_episodes = 100001
    pre_train_steps = 20000 * max_epLength
    annealing_steps = 60001 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = sarCen.Agent

class SarsaCenTwo(object):
    name = "sarsaCen200"
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.001
    update_freq = None
    batch_size = None
    # num_episodes = 62501
    # pre_train_steps = 0 * max_epLength
    # annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    num_episodes = 200001
    pre_train_steps = 60000 * max_epLength
    annealing_steps = 120001 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = sarCen.Agent


class SarsaDecMaliasNoPT(object):
    name = "sarsaDecGenMalialis"
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = None
    batch_size = None
    num_episodes = 62501#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = sarCen.Agent
    group_size = 1 # number of filters each agent controls

class SarsaDecMaliasNoPTLarge(object):
    name = "sarsaDecGenNoPTLarge"    
    
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = None
    batch_size = None
    num_episodes = 120001#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = sarCen.Agent
    group_size = 1 # number of filters each agent controls


class SarsaDecMaliasWithPT(object):
    name = "sarsaDecGenPT"
    
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = None
    batch_size = None
    # num_episodes = 62501
    # pre_train_steps = 0 * max_epLength
    # annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    num_episodes = 82501#82501
    pre_train_steps = 2000#2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 

    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = sarCen.Agent
    group_size = 1 # number of filters each agent controls

class SarsaDecPTLarge(object):
    name = "sarsaDecGenLarge"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = None #How often to perform a training step.
    batch_size = None #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 20000 * max_epLength #40000 * max_epLength #
    annealing_steps = 60000 * max_epLength  #120000 * max_epLength  #


    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = sarCen.Agent
    group_size = 1 # number of filters each agent controls



class SarsaGenericTeam(object):
    group_size = 2
    name = "Sarsa200TeamOf{0}".format(group_size)
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = None #How often to perform a training step.
    batch_size = None #How many experiences to use for each training step.
    num_episodes = 200001 #200001#    
    pre_train_steps = 40000 * max_epLength #40000 * max_epLength #
    annealing_steps = 120000 * max_epLength  #120000 * max_epLength  #
    
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = sarCen.Agent

class GeneralSettings(object):
    # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    SaveModelEnum = Enum('SaveModel', 'neither save load')
    debug = False
    # save_attack = SaveAttackEnum.neither
    save_model = SaveModelEnum.save




# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

"""
Settings to change


"""
assignedNetwork = NetworkSingleTeamMalialisMedium
assignedAgent = SarsaDoubleSingleCommunicate
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)



# sarsaGeneric = None

conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 




loadAttacks = False

if loadAttacks:
    for attackClass in attackClasses:
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        #genericAgent = None
        attack_location = load_attack_path+attackClass.getName()+".apkl"

        exp = experiment.Experiment(attackClass, GeneralSettings, assignedNetwork, 
            assignedAgent, twist= "", load_attack_path=attack_location)
        exp.run(0, genericAgent)
    getSummary(attackClasses, exp.load_path, assignedAgent)

else:
    experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent)
    # experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, "double")


    start_num = int(sys.argv[1])
    length_core= int(sys.argv[2])

    for i in range(length_core):
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        # genericAgent = None        
        print("Im doing it for {0}".format(start_num+i))
        experiment.run(start_num+i, genericAgent)



"""

for attackClass in attackClasses:
    sarsaGeneric = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
    # sarsaGeneric = None
    
    attack_location = load_attack_path+attackClass.getName()+".apkl"

    exp = experiment.Experiment(attackClass, GeneralSettings, assignedNetwork, 
        assignedAgent, twist= "NoPTTile1Save", load_attack_path=attack_location)
    exp.run(0, sarsaGeneric)
"""

"""


exp = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, 
    assignedAgent, load_attack_path=None)


start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

for i in range(length_core):
    sarsaGeneric = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
    print("Im doing it for {0}".format(start_num+i))
    exp.run(start_num+i, sarsaGeneric)
    # exp.run(start_num+i)

"""



