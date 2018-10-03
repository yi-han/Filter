import sys
import experiment
import network.hosts as hostClass
import agent.ddqnCentralised as ddCen

#import generic_run



import agent.ddqnCentralised as ddCen
# import agent.ddqnDecentralised as ddDec

from mapsAndSettings import *
assert(len(sys.argv)==3)

class ddqnCenSettings(object):
    
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

 
class ddqnDoubleTeamTwo(object):
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
    group_size = 2

class GeneralSettings(object):
    # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    SaveModelEnum = Enum('SaveModel', 'neither save load test')
    #test = False # handled by saveModel
    debug = False
    #load_model = False
    # save_attack = SaveAttackEnum.neither
    save_model = SaveModelEnum.save


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 


assignedNetwork = NetworkFourTeamThreeAgent
assignedAgent = ddqnCenDoubleSettings
load_attack_path = "attackSimulations/malialis_small/"
# load_attack_path = None

genericAgent = create_generic_dec(ddqnDoubleTeamTwo, GeneralSettings, NetworkFourTeamThreeAgent)
# genericAgent = None

"""
for attackClass in attackClasses:
    genericAgent = create_generic_dec(ddqnDoubleTeamTwo, GeneralSettings, NetworkFourTeamThreeAgent)

    attack_location = load_attack_path+attackClass.getName()+".apkl"

    exp = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, 
        assignedAgent, twist= "doubleSave", load_attack_path=attack_location)
    exp.run(0, genericAgent)
"""


experiment = experiment.Experiment(conAttack, GeneralSettings, NetworkFourTeamThreeAgent, ddqnDoubleTeamTwo, twist="double")
# experiment = experiment.Experiment(conAttack, GeneralSettings, NetworkFourThrottle, ddqnCenDoubleSettings, "double")


start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

for i in range(length_core):
    print("Im doing it for {0}".format(start_num+i))
    experiment.run(start_num+i, genericAgent)
