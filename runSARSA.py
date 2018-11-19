import sys
import experiment
import network.hosts as hostClass
from network.network_new import stateRepresentationEnum # how to represent the state
import agent.tileCoding as tileCoding
import agent.sarsaCentralised as sarCen
import agent.linearSarsaCentralised as linCen
import agent.randomAgent as ranAg
#import agent.sarsaDecentralised as sarDec# import agent.ddqnDecentralised as ddDec
from mapsAndSettings import *
assert(len(sys.argv)>=3)

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

    #stateletFunction = getStateletWithCommunication
    isCommunication = True # flag to demonstrate communication  
    reward_overload = False


class SarsaDecMaliasOriginal(object):
    name = "sarsaDecGenMalialisOriginal"
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
    #stateletFunction = getStateletNoCommunication
    #isCommunication = False
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.throttler 

class SarsaCTL(object):
    name = "sarsaCTL"
    max_epLength = 30 # or 60 if test
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
    sub_agent = sarCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    #isCommunication = False
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate

class SarsaDecMaliasNoPT(object):
    name = "sarsaDecGenMalialisNoOpt"
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
    #stateletFunction = getStateletNoCommunication
    isCommunication = False
    reward_overload = None

class LinearSarsaSingular(object):
    name = "LinearSarsaSingular"
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
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.throttler  

class LinearSarsaLong(LinearSarsaSingular):
    name = "LinearSarsaLong"
    num_episodes = 100001

class LinearSarsaLAI(object):
    name = "LinearSarsaLAI"
    max_epLength = 30 # or 60 if test
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
    sub_agent = linCen.Agent
    group_size = 1 # number of filters each agent controls
    #stateletFunction = getStateletNoCommunication
    reward_overload = -1
    stateRepresentation = stateRepresentationEnum.leaderAndIntermediate  

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

"""
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
"""


class SarsaGenericTeam(object):
    # if you end up using this its to demonstrate why centralisation
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
    tileFunction = None




# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

"""
Settings to change


"""
assignedNetwork = NetworkMalialisSmall
assignedAgent = LinearSarsaSingular
load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)


maxThrottlerBandwidth = assignedNetwork.rate_attack_high * 3 # a throttler doesn't face more than 3
numTiles = 18
numTilings = 8
tileCoder = tileCoding.myTileInterface(maxThrottlerBandwidth, numTiles, numTilings)
#tileFunction = tileCoder.myTiles
GeneralSettings.encoders = [tileCoder]
if assignedAgent.stateRepresentation in [stateRepresentationEnum.leaderAndIntermediate,  stateRepresentationEnum.server]:
    print("providing the leader and intermediate")
    intermediateBandwidth = maxThrottlerBandwidth*2 # as intermediate has max 2 throttlers
    GeneralSettings.encoders.append(tileCoding.myTileInterface(intermediateBandwidth, numTiles, numTilings))
    leaderBandwidth = maxThrottlerBandwidth * 6
    GeneralSettings.encoders.append(tileCoding.myTileInterface(leaderBandwidth, numTiles, numTilings))

elif assignedAgent.stateRepresentation == stateRepresentationEnum.server:
    serverMaxBandiwidth = len(assignedNetwork.host_sources)*assignedNetwork.rate_attack_high
    GeneralSettings.encoders.append(tileCoding.myTileInterface(serverMaxBandiwidth, numTiles, numTilings))
elif assignedAgent.stateRepresentation == stateRepresentationEnum.allThrottlers:
    #note this is an inefficietn cheap way. Use the better way if you do this
    for i in (range(len(assignedNetwork.host_sources))-1):
        GeneralSettings.encoders.append(tileCoding.myTileInterface(maxThrottlerBandwidth, numTiles, numTilings))
# sarsaGeneric = None

conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 

if len(sys.argv)==4:
    partition = sys.argv[3]
else:
    partition = ""


loadAttacks = False

if loadAttacks:
    for attackClass in attackClasses:
        genericAgent = create_generic_dec(assignedAgent, GeneralSettings, assignedNetwork)
        #genericAgent = None
        attack_location = load_attack_path+attackClass.getName()+".apkl"

        exp = experiment.Experiment(attackClass, GeneralSettings, assignedNetwork, 
            assignedAgent, twist= "Alias{0}".format(partition), load_attack_path=attack_location)
        exp.run(0, genericAgent)
    getSummary(attackClasses, exp.load_path, assignedAgent)

else:
    experiment = experiment.Experiment(conAttack, GeneralSettings, assignedNetwork, assignedAgent, twist="withReducedTileCoding{0}Alias{1}".format(numTiles, partition))
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



