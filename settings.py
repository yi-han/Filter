import experiment
from enum import Enum
import network.hosts as hostClass


# list of agents to choose
# from agent.sarsaCentralised import *
from agent.sarsaDecentralised import *
# from agent.ddqnCentralised import *
# from agent.ddqnDecentralised import *



class TrainSettings(object):
    max_epLength = 30 # or 60 if test
    y = 0


class sarsaDecMalias(object):
    
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = None
    batch_size = None
    # num_episodes = 62501
    # pre_train_steps = 0 * max_epLength
    # annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    num_episodes = 11001
    pre_train_steps = 0 * max_epLength
    annealing_steps = 1001 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = Agent


class ddqnCenSettings(object):
    
    max_epLength = 30 # or 60 if test
    y = 0    
    tau = 0.001 #Rate to update target network toward primary network. 
    update_freq = 4 #How often to perform a training step.
    batch_size = 32 #How many experiences to use for each training step.
    num_episodes = 100001    
    pre_train_steps = 20000 * max_epLength
    annealing_steps = 60000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    
    startE = 1
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps

### Network Settings. Put this in a class/ object?

class NetworkBasic(object):
    N_state = 3 #The number of state, i.e., the number of filters
    N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_agent = 10 # each filter can do 10 actions
    N_switch = 13 # number of routers in the system
    host_sources = [5, 10, 12, 6, 9, 9] #ID of the switch that the host is connected to  

    servers = [0] #ID of the switch that the server is connected to 
    filters = [5, 6, 9] #ID of the switch that the filter locates at

    topologyFile = 'topology.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 8
    iterations_between_action = 5





# The class of the adversary to implement
adversary = hostClass.ConstantAttack
# adversary = hostClass.ShortPulse
# adversary = hostClass.MediumPulse
# adversary = hostClass.LargePulse
# adversary = hostClass.GradualIncrease


SaveAttackEnum = Enum('SaveAttack', 'neither save load')
save_attack_path = "./attack.pkl" # note you shouldn't be repeating this


test = False
debug = False
load_model = False
repeats = 1
save_attack = SaveAttackEnum.neither


experiment = experiment.Experiment(save_attack_path, test, debug, save_attack, SaveAttackEnum, adversary, NetworkBasic, sarsaDecMalias)

experiment.run(2)
"""
Aim to only change settings here and feed into experiment


"""


"""
Malialis. Use the same settings as Router Throttling Experiment
"""


"""
2060

20000 pretrain
60000 annealing
20000 exploitation

e 1->0


"""






