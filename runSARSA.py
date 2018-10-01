import sys
import experiment
import network.hosts as hostClass

import agent.sarsaCentralised as sarCen
import agent.sarsaDecentralised as sarDec# import agent.ddqnDecentralised as ddDec
import agent.genericDecentralised as genericDecentralised
from networkSettings import *
assert(len(sys.argv)==3)
import math

def create_generic_dec_sarsa(gs, general_s, ns, sub_agent, group_size):
    """
    gs = generic_settings, ns = network_settings

    """
    throttlers_not_allocated = ns.N_state
    num_teams = math.ceil(ns.N_state/group_size)

    sub_agent_list = []

    test = (general_s.save_model is general_s.SaveModelEnum.test)
    print(sub_agent)
    while throttlers_not_allocated > 0:
        print("currently {0} throttlers_not_allocated".format(throttlers_not_allocated))
        agent_to_allocate = min(throttlers_not_allocated, group_size)
        sub_agent_list.append(sub_agent(ns.action_per_throttler**agent_to_allocate, gs.pre_train_steps,
            ns.action_per_throttler, agent_to_allocate, gs.tau, gs.y, general_s.debug,
            test))
        throttlers_not_allocated -= agent_to_allocate

    #print("\nTest {0} \n".format(sub_agent_list[0].N_action))
    master = genericDecentralised.AgentOfAgents(
        ns.N_action, gs.pre_train_steps, ns.action_per_throttler, ns.N_state,
            sub_agent_list, gs.tau, gs.y, general_s.debug, 
            test
        )
    return master

class SarsaCenMalias(object):
    
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
    
    max_epLength = 30 # or 60 if test
    y = 0
    tau = 0.1
    update_freq = None
    batch_size = None
    # num_episodes = 62501
    # pre_train_steps = 0 * max_epLength
    # annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    num_episodes = 62501#82501
    pre_train_steps = 0#2000 * max_epLength
    annealing_steps = 50000 * max_epLength #1000*max_epLength #60000 * max_epLength 
    

    startE = 0.4 #0.4
    endE = 0.0
    stepDrop = (startE - endE)/annealing_steps
    agent = sarDec.Agent

class SarsaDecMaliasWithPT(object):
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
    agent = sarDec.Agent

class SarsaDecPTLarge(object):
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
    agent = sarDec.Agent    


class SarsaCenGeneric(object):
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
    agent = None

# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease



sarsaGeneric = create_generic_dec_sarsa(SarsaCenGeneric, GeneralSettings, NetworkSimpleBasic, sarCen.Agent, 1)

# experiment = experiment.Experiment(save_attack_path, test, debug, save_attack, SaveAttackEnum, conAttack, NetworkSimpleStandard, SarsaCenMalias)


experiment = experiment.Experiment(conAttack, GeneralSettings, NetworkSimpleBasic, SarsaCenGeneric, "LargeTile1")


start_num = int(sys.argv[1])
length_core= int(sys.argv[2])

for i in range(length_core):
    print("Im doing it for {0}".format(start_num+i))
    experiment.run(start_num+i, sarsaGeneric)





