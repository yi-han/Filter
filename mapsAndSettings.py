"""
Common settings for networks

"""

### Network Settings. Put this in a class/ object?

from enum import Enum
import math
import agent.genericDecentralised as genericDecentralised
import agent.sarsaCentralised as sarCen
from network.network_new import stateRepresentationEnum
import pandas

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

    max_hosts_per_level = [3] # no communication therefore just one


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
    upper_boundary = 12.5
    iterations_between_action = 5 

    max_hosts_per_level = [2, 6, 12]

class NetworkSixFour(NetworkSingleTeamMalialisMedium):
    # 4 attackers per throttler.
    name = "six_four"
    host_sources = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
    7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9]
    upper_boundary = 25
    max_hosts_per_level = [4, 12, 24]

class NetworkMalialisTeamFull(object):
    name = "full_team_malialias"
    N_state = 30
    N_action = 1000000000000000000000000000000
    action_per_throttler = 10
    N_switch = 47
    host_sources = [4, 4, 5, 5, 6, 6, 44, 44, 45, 45, 46, 46, 
    9, 9, 10, 10, 11, 11, 13, 13, 14, 14, 15, 15, 
    18, 18, 19, 19, 20, 20, 22, 22, 23, 23, 24, 24,
    27, 27, 28, 28, 29, 29, 31, 31, 32, 32, 33, 33,
    36, 36, 37, 37, 38, 38, 40, 40, 41, 41, 42, 42]

    servers = [0]
    filters = [4, 5, 6, 44, 45, 46,
    9, 10, 11, 13, 14, 15,
    18, 19, 20, 22, 23, 24,
    27, 28, 29, 31, 32, 33,
    36, 37, 38, 40, 41, 42]

    topologyFile = 'topologies/full_team.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 12.5
    iterations_between_action = 5 
    max_hosts_per_level = [2, 6, 12, 60]    


class NetworkTwelveThrottleLight(object):
    name = "network_twelve_throttle_light"
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
    upper_boundary = 45#52
    iterations_between_action = 5     



class NetworkTwelveThrottleHeavy(object):
    name = "network_twelve_throttle_heavy"
    N_state = 12
    N_action = int(1e12)

    action_per_throttler = 10
    N_switch = 19
    host_sources = [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 
    7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 
    12, 12, 12, 12, 12, 13, 13, 13, 13, 13,
    14, 14, 14, 14, 14, 16, 16, 16, 16, 16, 
    17, 17, 17, 17, 17, 18, 18, 18, 18, 18]
    servers = [0]
    filters = [3, 4, 5, 7, 8, 9, 12, 13, 14, 16, 17, 18]
    
    topologyFile = 'topologies/four_team_three_agent.txt'
    rate_legal_low = 0.05 
    rate_legal_high = 1 
    rate_attack_low = 2.5 
    rate_attack_high = 6
    legal_probability = 0.6 # probability that is a good guys
    upper_boundary = 45#52
    iterations_between_action = 5 




def create_generic_dec(gs, general_s, ns):
    """
    gs = generic_settings, ns = network_settings

    We can make agents into groups.

    """
    throttlers_not_allocated = ns.N_state
    group_size = gs.group_size
    sub_agent = gs.sub_agent
    #num_teams = math.ceil(ns.N_state/group_size)
    #stateletFunction = gs.stateletFunction
    sub_agent_list = []

    test = (general_s.save_model is general_s.SaveModelEnum.load)
    print(sub_agent)
    while throttlers_not_allocated > 0:
        print("currently {0} throttlers_not_allocated".format(throttlers_not_allocated))
        agent_to_allocate = min(throttlers_not_allocated, group_size)
        state_size = calcStateSize(ns.N_state, gs.stateRepresentation)
        print(agent_to_allocate)
        sub_agent_list.append(sub_agent(ns.action_per_throttler**agent_to_allocate, gs.pre_train_steps,
            ns.action_per_throttler, state_size, general_s.encoders, gs.tau, gs.y, general_s.debug,
            test))
        throttlers_not_allocated -= agent_to_allocate

    #print("\nTest {0} \n".format(sub_agent_list[0].N_action))
    master = genericDecentralised.AgentOfAgents(
        ns.N_action, gs.pre_train_steps, ns.action_per_throttler, ns.N_state,
            sub_agent_list, gs.tau, gs.y, general_s.debug, 
            test
        )
    return master



def getSummary(adversary_classes, load_path, agent):
    summary = open("{0}/attackSummary.csv".format(load_path), "w")
    summary.write("Attack Type, Agent, Legal Packets Received, Legal Packets Served, Percentage, Server Failures, tau, pretraining, annealing, total_episodes, start_e, overload\n")
    agentName = agent.name
    for adversary_class in adversary_classes:
        attack_type = adversary_class.getName()
        file_path = "{0}/packet_served-{1}-{2}-{3}.csv".format(load_path,"test", attack_type, 0)
        packet_file = pandas.read_csv(file_path)
        #print(packet_file)
        sum_packets_received = sum(packet_file.PacketsReceived)
        sum_packets_sent = sum(packet_file.PacketsServed)
        sum_server_failures = sum(packet_file.ServerFailures)
        percentage_received = sum_packets_received/sum_packets_sent*100
        tau = agent.tau
        pretraining = agent.pre_train_steps / agent.max_epLength
        annealing = agent.annealing_steps / agent.max_epLength
        total_episodes = agent.num_episodes
        start_e = agent.startE
        if agent.reward_overload==-1:
            overload = '-1'
        elif agent.reward_overload == None:
            overload = 'None'
        else:
            overload = 'misc'

        summary.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}\n".format(attack_type, agent.name,
            sum_packets_received, sum_packets_sent, percentage_received, sum_server_failures,
            tau, pretraining, annealing, total_episodes, start_e, overload))
    summary.close()



# def getStateletNoCommunication(state, sizeOfSegment):
#     # get a segment of state corresponding to the agent, return remaining state as well
#     statelet = state[0:sizeOfSegment]
#     remainingState = state[sizeOfSegment:]
#     return (statelet, remainingState)


# def getStateletWithCommunication(state, sizeOfSegment):
#     return (state, state)


# def calcStateSize(size_of_group, total_number_states, isCommunication):
#     if isCommunication:
#         return total_number_states
#     else:
#         return size_of_group

def calcStateSize(total_throttlers, stateRepresentation):
    if stateRepresentation == stateRepresentationEnum.throttler:
        return 1
    elif stateRepresentation == stateRepresentationEnum.leaderAndIntermediate:
        return 3
    elif stateRepresentation == stateRepresentationEnum.server:
        return 4
    elif stateRepresentation == stateRepresentationEnum.allThrottlers:
        return total_throttlers
    else:
        assert(1==2)

