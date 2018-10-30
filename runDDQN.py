import sys
import experiment
import network.hosts as hostClass
import agent.ddqnCentralised as ddCen

#import generic_run



import agent.ddqnCentralised as ddCen
# import agent.ddqnDecentralised as ddDec

from mapsAndSettings import *
assert(len(sys.argv)==4)

class ddqnCenSettings(object):
    name = "DDQNCentralised100"
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 100001 #200001#    
    pre_train_steps = 20000 * max_epLength #40000 * max_epLength #
    annealing_steps = 60000 * max_epLength  #120000 * max_epLength  #
    
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = ddCen.Agent

class ddqnCenDoubleSettings(object):
    name = "DDQNCentralised200"
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
    agent = ddCen.Agent

""" 
class ddqnDoubleTeamGeneric(object):
    group_size = 2
    name = "DDQN200TeamOf{0}".format(group_size)
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

    stateletFunction = getStateletNoCommunication
    isCommunication = False
"""
class ddqnDoubleSingleCommunicate(object):
    group_size = 1
    name = "DDQN200SingleFullCommunicate"
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
    # stateletFunction = getStateletWithCommunication
    isCommunication = True # flag to demonstrate communication    
    reward_overload = None

class ddqnDoubleHierarchical(object):
    group_size = 1
    name = "DDQN200"
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
    annealing_steps = 600000 * max_epLength  #120000 * max_epLength  #
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = None
    sub_agent = ddCen.Agent
    # stateletFunction = getStateletNoCommunication
    stateRepresentation = stateRepresentationEnum.throttler
    reward_overload = None

class ddqnSingleSarsaCopy(object):
    # apart from 2000 pretrain this is as close as it gets
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




class GeneralSettings(object):
    # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    SaveModelEnum = Enum('SaveModel', 'neither save load test')
    #test = False # handled by saveModel
    debug = False
    #load_model = False
    # save_attack = SaveAttackEnum.neither
    save_model = SaveModelEnum.save
    tileFunction = None


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 


assignedNetwork = NetworkSingleTeamMalialisMedium
assignedAgent = ddqnSingleNoCommunicate
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
loadAttacks = False
# genericAgent = None

#partition = sys.argv[3] #ignore
if loadAttacks:
    for attackClass in attackClasses:
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        # genericAgent = None
        attack_location = load_attack_path+attackClass.getName()+".apkl"

        exp = experiment.Experiment(attackClass, GeneralSettings, assignedNetwork, 
            assignedAgent, twist= "", load_attack_path=attack_location)
        exp.run(0, genericAgent)

    getSummary(attackClasses, exp.load_path, assignedAgent)
else:
    experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="")
    # experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, "double")


    start_num = int(sys.argv[1])
    length_core= int(sys.argv[2])

    for i in range(length_core):
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        # genericAgent = None        
        print("Im doing it for {0}".format(start_num+i))
        experiment.run(start_num+i, genericAgent)


