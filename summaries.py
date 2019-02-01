import sys

import os
import numpy as np
import pandas

def massSummary(load_path):
    """
    Go through the packet data and make some stats showing actual distributions.

    We assume that prior summaries are deleted except the relevent one. 
    We use this to provide contextual information about the agent / advesary.
    """
    ms = open("{0}/attack_summary_mass.csv".format(load_path), "w")
    ms.write("AttackType,Repeats,Agent,Drift,MeanPercentage,Range,SD,Tau,Pretraining,Annealing,TotalEpisodes,start_e,overload,adv_tau,adv_discount,adv_pretrain,adv_annealing_episodes,adv_episodes,adv_start_e\n")
    # Open up the first summary

    init_summary_path = "{0}/attackSummary-0.csv".format(load_path)
    init_summary = pandas.read_csv(init_summary_path)
    num_attacks = len(init_summary['AttackType'])
    agent_used = init_summary.iloc[-1]["Agent"]
    drift = init_summary.iloc[-1]["Drift"]
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
            packet_file.readline()       
            for line in packet_file.readlines():
                line = line.split(",")
                attacker = line[0]
                percentage = line[5]
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
            ms.write("{0},{1},".format(agent_used, drift))

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

assert(len(sys.argv)>1)
massSummary(sys.argv[1])
print("done")