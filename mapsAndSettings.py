"""
Common settings for networks

"""

### Network Settings. Put this in a class/ object?

from enum import Enum
import math
import agent.genericDecentralised as genericDecentralised
import adversary.ddAdvGenericMaster as ddGeneric
import adversary.ddAdvGenericAgent as ddGenAgent
import adversary.sarsaAdvAgent as sarsaAdvAgent
import adversary.dumbMaster as dumbMaster
import adversary.dumbAgent as dumbAgent
import pandas
from network.utility import *
import network.hosts as hosts
import agent.AIMD
import os
import numpy as np
import pandas

# defender_mode_enum = Enum('SaveModel', 'neither save load test_short')

class defender_mode_enum(Enum):
    neither = 0
    save = 1
    load = 2
    test_short = 3
    load_save = 4 # for using a pre-made policy and continuing
    load_continue = 5 # more for continuing one done half way
    
class stateRepresentationEnum(Enum):
    throttler = 0 #always
    leaderAndIntermediate = 1 
    server = 2  # all the way to the server
    allThrottlers = 3
    only_server = 4



class adv_constant(object):
    name = "constant_attack"
    
    adversary_class = dumbMaster.dumbMaster
    adv_agent_class = dumbAgent.dumbAgent    
    is_intelligent = False
    num_adv_agents = 2
    attack_strategy = advesaryStandardAttackEnum.constant
    endE = 0
    startE = 0

class adv_singular_constant_attack(adv_constant):
    name = "singular_constant_attack"
    num_adv_agents = 1

class adv_pulse_short(adv_constant):
    name = "pulse_short"
    attack_strategy = advesaryStandardAttackEnum.pulse_short

class adv_pulse_medium(adv_constant):
    name = "pulse_medium"
    attack_strategy = advesaryStandardAttackEnum.pulse_medium

class adv_pulse_large(adv_constant):
    name = "pulse_large"
    attack_strategy = advesaryStandardAttackEnum.pulse_large

class adv_gradual(adv_constant):
    name = "gradual"
    attack_strategy = advesaryStandardAttackEnum.gradual

class adv_split(adv_constant):
    name = "split"
    attack_strategy = advesaryStandardAttackEnum.split

class adv_random(adv_constant):
    name = "random"
    attack_strategy = advesaryStandardAttackEnum.random

class AIMDsettings(object):
    name = "AIMD"
    group_size = 1
    delta = 0.35 # additive increase
    beta = 2 # multiplicative decrease
    epsilon = 0.001
    stateRepresentation = stateRepresentationEnum.only_server # WRONG
    sub_agent = agent.AIMD.AIMDagent

    num_episodes = 1
    y = delta
    tau = beta
    update_freq = None
    batch_size = None
    pre_train_episodes = 0
    annealing_episodes = 0
    startE = 0
    endE = 0
    stepDrop = 0
    reward_overload = None
    has_bucket = True

# class AIMDvariant(AIMDsettings):
#     name = "AIMDvariant"
#     sub_agent = agent.AIMD.AIMDvariant



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
    lower_boundary = 6 # for AIMD
    iterations_between_action = 40 #200

    max_hosts_per_level = [3] # no communication therefore just one
    bucket_capacity = 18.1#15#0.8

    max_epLength = 30
    is_sig_attack = False
    save_per_step_stats = False

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
    upper_boundary = 14 #12.5 # Mal would have used 14
    lower_boundary = 10 # for AIMD

    iterations_between_action = 30 #30 # 200

    max_hosts_per_level = [2, 6, 12]
    bucket_capacity = 12.1
    max_epLength = 30

    is_sig_attack = False
    save_per_step_stats = False


class NetworkSixFour(NetworkSingleTeamMalialisMedium):
    # 4 attackers per throttler.
    name = "six_four"
    host_sources = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
    7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9]
    upper_boundary = 26 # malialis would have used 26
    lower_boundary = 18 # malialis would have used 20
    max_hosts_per_level = [4, 12, 24]
    bucket_capacity = 24.1


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
    upper_boundary = 62
    lower_boundary = 56
    iterations_between_action = 20
    max_hosts_per_level = [2, 6, 12, 60]    
    bucket_capacity = 12
    is_sig_attack = False
    max_epLength = 30
    save_per_step_stats = False

### This is an experimental one where i have not set an even set of hosts
# class NetworkMalialisTeamFull(object):
#     name = "full_team_malialias"
#     N_state = 30
#     N_action = 1000000000000000000000000000000
#     action_per_throttler = 10
#     N_switch = 47
#     host_sources = [4, 4, 4, 5, 6, 6, 44, 44, 44, 45, 46, 46, 
#     9, 10, 10, 10, 11, 11, 13, 14, 14, 14, 15, 15, 
#     18, 18, 19, 20, 20, 20, 22, 22, 23, 24, 24, 24,
#     27, 28, 28, 28, 29, 29, 31, 32, 32, 32, 33, 33,
#     36, 36, 36, 37, 38, 38, 40, 40, 40, 41, 42, 42]

#     servers = [0]
#     filters = [4, 5, 6, 44, 45, 46,
#     9, 10, 11, 13, 14, 15,
#     18, 19, 20, 22, 23, 24,
#     27, 28, 29, 31, 32, 33,
#     36, 37, 38, 40, 41, 42]

#     topologyFile = 'topologies/full_team.txt'
#     rate_legal_low = 0.05 
#     rate_legal_high = 1 
#     rate_attack_low = 2.5 
#     rate_attack_high = 6
#     legal_probability = 0.6 # probability that is a good guys
#     upper_boundary = 62
#     lower_boundary = 56
#     iterations_between_action = 10
#     max_hosts_per_level = [2, 6, 12, 60]   





class DdGenericDec(object):
    name = "dd DO NOT USE"
    num_adv_agents = -1
    pre_train_episodes = 50000
    annealing_episodes = 200000
    num_episodes = 500000
    tau = 0.0005
    discount_factor = 0.6
    startE = 1
    endE = 0.0
    
    packets_last_step = False
    prior_server_loads = 0
    prior_agent_actions = 5
    prior_adversary_actions = 5
    include_indiv_hosts = False    
    prior_agent_delta_moves = 0
    include_legal_traffic = False
    prior_server_percentages = 0

    is_intelligent = True
    update_freq = 4
    batch_size = 32
    adversary_class = ddGeneric.GenericAdvMaster
    adv_agent_class = ddGenAgent.ddGenAgent
    action_per_agent = 11
    include_other_attackers = False
    include_encoder = False

class ddTest(DdGenericDec):
    name = "ddTest"
    num_adv_agents =1
    pre_train_episodes = 2
    annealing_episodes = 4
    num_episodes = 20

class DdGenericCentral(DdGenericDec):
    name = "ddGenCentral"
    num_adv_agents = 1
    pre_train_episodes = 50000
    include_other_attackers = False



class DdGenericSplit(DdGenericDec):
    name = "ddGenSplit"
    num_adv_agents = 2
    include_other_attackers = False
    num_episodes = 600000

class ddExpThree(DdGenericDec):
    name = "ddExpThree"
    num_adv_agents = 2
    include_other_attackers = False
    pre_train_episodes = 50000
    annealing_episodes = 300000
    num_episodes = 600000 


class ddAimd(DdGenericDec):
    num_adv_agents = 1
    name = "ddAimd"
    prior_adversary_actions = 6
    
    prior_agent_actions = 0
    prior_agent_delta_moves = 6
    prior_server_loads = 0 
    prior_server_percentages = 0


    discount_factor = 0.6    
    pre_train_episodes = 50000
    annealing_episodes = 150000
    num_episodes = 350000

class ddAimd2(ddAimd):
    num_adv_agents = 1
    name = "ddAimd2"
    prior_adversary_actions = 6

    pre_train_episodes = 100000
    annealing_episodes = 300000
    num_episodes = 500000

class ddAimd3(ddAimd2):
    name = "ddAimd3"
    discount_factor = 0.3

class ddAimdAlt1(DdGenericDec):
    num_adv_agents = 1
    name = "ddAimdAlt1"
    prior_adversary_actions = 6
    
    prior_agent_actions = 0
    prior_agent_delta_moves = 6
    prior_server_loads = 0 
    prior_server_percentages = 6


    discount_factor = 0.6    
    pre_train_episodes = 50000
    annealing_episodes = 150000
    num_episodes = 350000

class ddAimdAlt2(ddAimdAlt1):
    num_adv_agents = 1
    name = "ddAimdAlt2"

    pre_train_episodes = 100000
    annealing_episodes = 300000
    num_episodes = 500000

class ddAimdAlt3(ddAimdAlt2):
    name = "ddAimdAlt3"
    discount_factor = 0.3

class ddAimdLarge(DdGenericDec):
    num_adv_agents = 1
    name = "ddAimdLarge"
    prior_adversary_actions = 6
    include_legal_traffic = True
    
    prior_agent_actions = 6
    prior_agent_delta_moves = 6
    prior_server_loads = 6
    prior_server_percentages = 6


    discount_factor = 0.6    
    pre_train_episodes = 50000
    annealing_episodes = 150000
    num_episodes = 350000

class ddAimdLarge2(ddAimdLarge):
    name = "ddAimdLarge2"
    pre_train_episodes = 100000
    annealing_episodes = 300000
    num_episodes = 500000    
   
class ddAimdLarge3(ddAimdLarge2):
    name = "ddAimdLarge3"
    discount_factor = 0.3


# class ddAimdAExtended(DdGenericDec):
#     num_adv_agents = 1

#     name = "ddAimdAExtended"
#     prior_agent_delta_moves = 10
#     prior_agent_actions = 10
#     prior_adversary_actions = 10
#     include_indiv_hosts = True  

#     packets_last_step = True
#     discount_factor = 0.6

# class ddAimdExtProper(DdGenericDec):
#     num_adv_agents = 1
#     name = "ddAimdProper"
#     prior_agent_delta_moves = 7
#     prior_agent_actions = 7
#     prior_adversary_actions = 7
#     prior_server_loads = 7
#     include_legal_traffic = True
 
#     discount_factor = 0.5

#     pre_train_episodes = 50000
#     annealing_episodes = 150000
#     num_episodes = 350000

class sarGenericDec(object):
    name = "sarsaGenericDec"
    num_adv_agents = -1
    pre_train_episodes = 75000
    annealing_episodes = 300000
    num_episodes = 750000
    tau = 0.001
    discount_factor = 0.6
    startE = 1
    endE = 0.0
    
    prior_agent_actions = 5
    prior_adversary_actions = 5   
    packets_last_step = False
    include_indiv_hosts = False    
    prior_agent_delta_moves = 0
    prior_server_loads = 0
    prior_server_percentages = 0

    include_legal_traffic = False

    is_intelligent = True
    max_epLength = None
    reward_overload = None
    update_freq = 4
    batch_size = 32
    adversary_class = ddGeneric.GenericAdvMaster
    adv_agent_class = sarsaAdvAgent.sarGenAgent
    action_per_agent = 11
    include_other_attackers = False    
    include_encoder = True

class sarGenericCen(sarGenericDec):
    name = "sarsaGenericCen"
    num_adv_agents = 1



class sarAdvSplit(sarGenericCen):
    name = "sarsaAdvSplit"
    num_adv_agents = 2 

class sarAdvExpThree(sarGenericCen):
    name = "sarsaAdvExpThree"
    num_adv_agents = 2 
    pre_train_episodes = 50000
    annealing_episodes = 300000
    num_episodes = 600000    



class sarAimd(sarGenericDec):
    num_adv_agents = 1
    name = "sarAimd"
    prior_agent_delta_moves = 5
    prior_agent_actions = 0
    packets_last_step = False
    discount_factor = 0.6

    pre_train_episodes = 75000
    annealing_episodes = 225000
    num_episodes = 500000

class sarAimd2(sarAimd):
    name = "sarAimd2"
    pre_train_episodes = 75000
    annealing_episodes = 225000
    num_episodes = 500000    

class sarAimd3(sarAimd2):
    name = "sarAimd3"
    discount_factor = 0.3

class sarAimdAlt1(sarGenericDec):
    num_adv_agents = 1
    name = "sarAimdAlt1"
    prior_agent_delta_moves = 5
    prior_agent_actions = 0
    prior_adversary_actions = 5
    prior_server_loads = 0    
    prior_server_percentages = 5
    include_legal_traffic = False
    discount_factor = 0.6

class sarAimdAlt2(sarAimdAlt1):
    name = "sarAimdAlt2"
    pre_train_episodes = 75000
    annealing_episodes = 225000
    num_episodes = 500000  

class sarAimdAlt3(sarAimdAlt2):
    name = "sarAimdAlt3"
    discount_factor = 0.3

class sarAimdLarge(sarGenericDec):
    num_adv_agents = 1
    name = "sarAimdLarge"
    prior_agent_delta_moves = 5
    prior_agent_actions = 5
    prior_adversary_actions = 5
    prior_server_loads = 5   
    prior_server_percentages = 5
    include_legal_traffic = True
    discount_factor = 0.6

class sarAimdLarge2(sarAimdLarge):
    name = "sarAimdLarge2"
    pre_train_episodes = 75000
    annealing_episodes = 225000
    num_episodes = 500000 

class sarAimdLarge3(sarAimdLarge2):
    name = "sarAimdLarge3"
    discount_factor = 0.3

def create_generic_dec(ds, ns):
    """
    ds = defender_settings, ns = network_settings

    We can make agents into groups.

    """

    if "AIMD" in ds.name:
        return ds.sub_agent(ns, ds)

    throttlers_not_allocated = ns.N_state

    group_size = ds.group_size
    sub_agent = ds.sub_agent
    #num_teams = math.ceil(ns.N_state/group_size)
    #stateletFunction = ds.stateletFunction
    sub_agent_list = []

    print(sub_agent)
    while throttlers_not_allocated > 0:
        print("currently {0} throttlers_not_allocated".format(throttlers_not_allocated))
        agent_to_allocate = min(throttlers_not_allocated, group_size)
        state_size = calcStateSize(ns.N_state, ds.stateRepresentation)
        print(agent_to_allocate)
        sub_agent_list.append(sub_agent(ns.action_per_throttler**agent_to_allocate, state_size, ds.encoders, ds))
        throttlers_not_allocated -= agent_to_allocate

    #print("\nTest {0} \n".format(sub_agent_list[0].N_action))
    master = genericDecentralised.AgentOfAgents(
        ns.N_action, ns.action_per_throttler, ns.N_state,
            sub_agent_list, ds.tau, ds.discount_factor
        )
    return master



def getSummary(adversary_classes, load_path, agent, prefix):
    summary = open("{0}/attackSummary-{1}.csv".format(load_path,prefix), "w")
    summary.write("AttackType,Agent,LegalPacketsReceived,LegalPacketsServed,Percentage,ServerFailures,Tau,Pretraining,Annealing,TotalEpisodes,start_e,overload,illegalSent,adv_tau,adv_discount,adv_pretrain,adv_annealing_episodes,adv_episodes,adv_start_e,delta,beta,epsilon,bucket_capacity, iteration\n")
    agentName = agent.name
    for adversary_class in adversary_classes:
        attack_name = adversary_class.name

        file_path = "{0}/packet_served-{1}-{2}-{3}.csv".format(load_path,agent.save_model_mode.name, attack_name, prefix)
        packet_file = pandas.read_csv(file_path)
        #print(packet_file)
        sum_legal_received = sum(packet_file.LegalReceived)
        sum_legal_sent = sum(packet_file.LegalSent)
        sum_server_failures = sum(packet_file.ServerFailures)
        adv_packets_sent = sum(packet_file.IllegalSent)
        percentage_received = sum_legal_received/sum_legal_sent*100
        tau = agent.tau
        pretraining = agent.pre_train_episodes
        annealing = agent.annealing_episodes
        total_episodes = agent.num_episodes
        start_e = agent.startE
        if agent.reward_overload==-1:
            overload = '-1'
        elif agent.reward_overload == None:
            overload = 'None'
        else:
            overload = 'misc'

        summary.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},".format(attack_name, agent.name,
            sum_legal_received, sum_legal_sent, percentage_received, sum_server_failures,
            tau, pretraining, annealing, total_episodes, start_e, overload, adv_packets_sent))
        if adversary_class.is_intelligent:
            summary.write("{0},{1},{2},{3},{4},{5},".format(adversary_class.tau, adversary_class.discount_factor,
                adversary_class.pre_train_episodes, adversary_class.annealing_episodes, adversary_class.num_episodes, adversary_class.startE))
        else:
            summary.write(",,,,,,")

        if agent.stateRepresentation == stateRepresentationEnum.only_server:
            summary.write("{0},{1},{2},".format(agent.delta, agent.beta, agent.epsilon))
            try:
                summary.write("{0},".format(agent.buck_value))
            except AttributeError:
                summary.write(",")
        else:
            summary.write(",,,")
        summary.write("{0}\n".format(prefix))
    summary.close()



def getPathName(network_settings, agent_settings, commStrategy, twist, train_opposition):
    # host train is the type of host the agent was trained on. 

    drift = network_settings.drift
    if drift > 0:
        drift_text = "Drift_{0}".format(drift)
    else:
        drift_text = ""
    return drift_text + train_opposition.name +"_" + network_settings.name + agent_settings.name + commStrategy  + twist




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


def calc_comm_strategy(stateRepresentation):
    if stateRepresentation == stateRepresentationEnum.throttler:
        return "Single"
    elif stateRepresentation == stateRepresentationEnum.leaderAndIntermediate:
        return "LeadAndInt"
    elif stateRepresentation == stateRepresentationEnum.server:
        return "IncludeServer"
    elif stateRepresentation == stateRepresentationEnum.allThrottlers:
        return "CommAll"
    else:
        return stateRepresentation.name


def merge_summaries(file_path):
    summary = open("{0}/attack_merged_summary.csv".format(file_path), "w")
    # we assume it goes from 0 to max
    first_summary = open("{0}/attackSummary-0.csv".format(file_path))
    header = first_summary.readline()
    summary.write(header)
    first_summary.close()

    #for i in range(0, number_summaries):
    i = 0
    while os.path.isfile("{0}/attackSummary-{1}.csv".format(file_path, i)):
        i_summary = open("{0}/attackSummary-{1}.csv".format(file_path, i))
        i_summary.readline()
        for line in i_summary.readlines():
            summary.write(line)
        i_summary.close()
        i+=1
    summary.close()

def massSummary(load_path):
    """
    Go through the packet data and make some stats showing actual distributions.

    We assume that prior summaries are deleted except the relevent one. 
    We use this to provide contextual information about the agent / advesary.
    """
    print(load_path)
    ms = open("{0}/attack_summary_mass.csv".format(load_path), "w")
    ms.write("AttackType,Repeats,Agent,MeanPercentage,Range,SD,Tau,Pretraining,Annealing,TotalEpisodes,start_e,overload,adv_tau,adv_discount,adv_pretrain,adv_annealing_episodes,adv_episodes,adv_start_e\n")
    # Open up the first summary

    init_summary_path = "{0}/attackSummary-0.csv".format(load_path)
    init_summary = pandas.read_csv(init_summary_path)
    num_attacks = len(init_summary['AttackType'])
    agent_used = init_summary.iloc[-1]["Agent"]
    tau = init_summary.iloc[-1]["Tau"]
    pretraining = init_summary.iloc[-1]["Pretraining"]
    annealing = init_summary.iloc[-1]["Annealing"]
    totalEpisodes = init_summary.iloc[-1]["TotalEpisodes"]
    start_e = init_summary.iloc[-1]["start_e"]
    overload = init_summary.iloc[-1]["overload"]
    adv_tau = init_summary.iloc[-1]["adv_tau"]
    adv_discount = init_summary.iloc[-1]["adv_discount"]
    adv_pretrain = init_summary.iloc[-1]["adv_pretrain"]
    adv_annealing_episodes = init_summary.iloc[-1]["adv_annealing_episodes"]
    adv_episodes = init_summary.iloc[-1]["adv_episodes"]
    adv_start_e = init_summary.iloc[-1]["adv_start_e"]

    # check number of rows to determine if advesary
    # grab agent / advesary details
    data_scores = {}
    attack_names = []
    first_file = True

    for prefix in range(20):
        print(prefix)
        packet_file_path = "{0}/attackSummary-{1}.csv".format(load_path, prefix)
        if os.path.exists(packet_file_path):
            packet_file = open(packet_file_path)
            #packet_pandas = pandas.read_csv(packet_file_path)

            header = packet_file.readline().split(",")
            attacker_index = header.index("AttackType")
            mean_percentage_index = header.index("Percentage")
            for line in packet_file.readlines():
                line = line.split(",")
                attacker = line[attacker_index]
                percentage = line[mean_percentage_index]
                if first_file:
                    # we're grabbing the attack names in order
                    attack_names.append(attacker)
                    data_scores[attacker] = []
                print("adding {0} to {1}".format(percentage, attacker))
                data_scores[attacker].append(float(percentage))

            first_file = False

    print(data_scores)
    for attack_name in attack_names:
        percentages = data_scores[attack_name]
        ms.write("{0},{1},".format(attack_name,len(percentages)))
        if len(percentages)>0:
            ms.write("{0},".format(agent_used))

            # calc and add mean, range,
            num_per = np.array(percentages) 
            print(num_per)
            print(num_per.mean())
            ms.write("{0},{1},{2},".format(num_per.mean(), num_per.ptp(), num_per.std()))

            ms.write("{0},{1},{2},{3},{4},{5},".format(tau, pretraining, annealing, totalEpisodes, start_e, overload))
            if attack_names.index(attack_name)>=5:
                ms.write("{0},{1},{2},{3},{4},{5}\n".format(adv_tau, adv_discount, adv_pretrain, adv_annealing_episodes, adv_episodes, adv_start_e))
            else:
                ms.write("{0},{1},{2},{3},{4},{5}\n".format("","","","","",""))
        else:
            for _ in range(17):
                ms.write(",")
            ms.write("\n")
    ms.close()