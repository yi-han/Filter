import experiment
from enum import Enum
import network.hosts as hostClass


# list of agents to choose
import agent.sarsaCentralised as sarCen
import agent.sarsaDecentralised as sarDec
import agent.ddqnCentralised as ddCen
import agent.ddqnDecentralised as ddDec



class sarsaCenMalias(object):
    
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


class sarsaDecMalias(object):
    
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = None
    batch_size = None
    # num_episodes = 62501
    # pre_train_steps = 0 * max_epLength
    # annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    num_episodes = 82501
    pre_train_steps = 2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = sarDec.Agent


class ddqnCenSettings(object):
    
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 100001    
    pre_train_steps = 20000 * max_epLength #20000 * max_epLength
    annealing_steps = 60000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = ddCen.Agent
### Network Settings. Put this in a class/ object?

class NetworkSimpleStandard(object):
    name = "simple_standard"
    N_state = 3 #The number of state, i.e., the number of filters
    N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_agent = 10 # each filter can do 10 actions
    N_switch = 13 # number of routers in the system
    host_sources = [5, 10, 12, 6, 9, 9] #ID of the switch that the host is connected to  

    servers = [0] #ID of the switch that the server is connected to 
    filters = [5, 6, 9] #ID of the switch that the filter locates at

    topologyFile = 'topologies/simple_standard.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 8
    iterations_between_action = 8

class NetworkSimpleBasic(object):
    name = "simple_basic"
    N_state = 2 #The number of state, i.e., the number of filters
    N_action = 100 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_agent = 10 # each filter can do 10 actions
    N_switch = 6 # number of routers in the system
    host_sources = [3, 4, 5] #ID of the switch that the host is connected to  

    servers = [0] #ID of the switch that the server is connected to 
    filters = [1, 2] #ID of the switch that the filter locates at

    topologyFile = 'topologies/simple_basic.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 8
    iterations_between_action = 5

class NetworkSimpleMedium(object):
    name = "simple_mediumUp12"

    N_state = 5 #The number of state, i.e., the number of filters
    N_action = 100000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_agent = 10 # each filter can do 10 actions
    N_switch = 13 # number of routers in the system
    host_sources = [3, 4, 5, 6, 7, 9, 10, 12, 12] #ID of the switch that the host is connected to  

    servers = [0] #ID of the switch that the server is connected to 
    filters = [3, 4, 9, 10, 12] #ID of the switch that the filter locates at

    topologyFile = 'topologies/simple_large.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 12
    iterations_between_action = 10

class NetworkMalialisMedium(object):
    name = "malialis_router_medium"

    N_state = 30
    N_action = 10**30
    action_per_agent = 10
    host_sources = [3, 3, 4, 4, 5, 5, 7, 7, 8, 8, 9, 9, 12, 12, 13, 13, 14, 14, \
        16, 16, 17, 17, 18, 18, 21, 21, 22, 22, 23, 23, 25, 25, 26, 26, 27, 27, \
        30, 30, 31, 31, 32, 32, 36, 36, 35, 35, ,34, 34, 39, 39, 40, 40, 41, 41, \
        43, 43, 44, 44, 45, 45]

    servers = [0]
    filters = [3, 4, 5, 7, 8, 9, 12, 13, 14, 16, 17, 18, 21, 22, 23, 25, 26, 27, \
        30, 31, 32, 34, 35, 36, 39, 40, 41, 43, 44, 45]

    topologyFile = None
    
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 62
    iterations_between_action = 5





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





# experiment = experiment.Experiment(save_attack_path, test, debug, save_attack, SaveAttackEnum, conAttack, NetworkSimpleStandard, sarsaCenMalias)
experiment = experiment.Experiment(conAttack, GeneralSettings, NetworkSimpleMedium, ddqnCenSettings)






