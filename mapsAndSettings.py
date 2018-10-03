"""
Common settings for networks

"""

### Network Settings. Put this in a class/ object?

from enum import Enum
import math
import agent.genericDecentralised as genericDecentralised
import agent.sarsaCentralised as sarCen


class NetworkSimpleBasic(object):
    name = "simple_basic"
    N_state = 2 #The number of state, i.e., the number of filters
    N_action = 100 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_throttler = 10 # each filter can do 10 actions
    N_switch = 3 # number of routers in the system
    host_sources = [1, 1, 2] #ID of the switch that the host is connected to  

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


class NetworkMalialisSmall(object):
    name = "malialis_small"
    N_state = 3 #The number of state, i.e., the number of filters
    N_action = 1000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_throttler = 10 # each filter can do 10 actions
    N_switch = 13 # number of routers in the system
    host_sources = [5, 10, 12, 6, 9, 9] #ID of the switch that the host is connected to  

    servers = [0] #ID of the switch that the server is connected to 
    filters = [5, 6, 9] #ID of the switch that the filter locates at

    topologyFile = 'topologies/malialis_original.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 8
    iterations_between_action = 10


class NetworkFourThrottle(object):
    # depreciated
    name = "four_throttlers"

    N_state = 4 #The number of state, i.e., the number of filters
    N_action = 10000 #In the current implementation, each filter has 10 possible actions, so altogether there are 10^N_state actions, 
                    #e.g., action 123 means the drop rates at the three filters are set to 0.1, 0.2 and 0.3, respectively
    action_per_throttler = 10 # each filter can do 10 actions
    N_switch = 8 # number of routers in the system
    host_sources = [3, 3, 4, 4, 6, 6, 7, 7] #ID of the switch that the host is connected to  

    servers = [0] #ID of the switch that the server is connected to 
    filters = [3, 4, 6, 7] #ID of the switch that the filter locates at

    topologyFile = 'topologies/four_throttlers.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 10
    iterations_between_action = 10

class NetworkSingleTeamMalialisMedium(object):
    name = "single_team_malialis_medium"
    N_state = 6
    N_action = 1000000

    action_per_throttler = 10
    N_switch = 10
    host_sources = [3, 3, 4, 4, 5, 5, 7, 7, 8, 8, 9, 9]
    servers = [0]
    filters = [3, 4, 5, 7, 8, 9]
    
    topologyFile = 'topologies/single_team_malialis.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 24#12.5
    iterations_between_action = 5 

class NetworkFourTeamThreeAgent(object):
    name = "four_Team_three_agent"
    N_state = 12
    N_action = int(1e12)

    action_per_throttler = 10
    N_switch = 19
    host_sources = [3, 3, 3, 4, 4, 4, 5, 5, 5, 7, 7, 7, 8, 8, 8, 9, 9, 9, 12, 12, 12, 13, 13, 13,
    14, 14, 14, 16, 16, 16, 17, 17, 17, 18, 18, 18]
    servers = [0]
    filters = [3, 4, 5, 7, 8, 9, 12, 13, 14, 16, 17, 18]
    
    topologyFile = 'topologies/four_team_three_agent.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 62#12.5
    iterations_between_action = 5     




def create_generic_dec(gs, general_s, ns):
    """
    gs = generic_settings, ns = network_settings

    """
    throttlers_not_allocated = ns.N_state
    group_size = gs.group_size
    sub_agent = gs.sub_agent
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



