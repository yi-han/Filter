"""
Running this file generates 500 attack episodes for each map for evaluation purposes

Attacks to be saved in list of lists of what generated, allow the network to
decide how to respond
"""
import sys
import network.network_new as netModule

import network.hosts as hostClass
import os#, sys, logging
import pickle
from mapsAndSettings import *


def generateAttacks(networkSettings, attackClasses, max_epLength = -1, num_episodes = 500):
    # For a given map (network settings) and set of attacks, generate attack episodes
    # We use default values to feed into the simulation engine 
    path = "attackSimulations/{0}/".format(networkSettings.name)

    reward_overload = -1
    networkSettings.is_sig_attack = True # ensure we only have significant attacks
    if not os.path.exists(path):
        os.makedirs(path)

    attack_path = path+"OneAndAQuarterAttack.apkl" 

    # just do it once 
    with open(attack_path, "wb") as f:
        
        # run all the simulations
        net = netModule.network_full(networkSettings, conAttack, AimdMalialis, None, None, True)
        for _ in range(num_episodes):
            net.reset()

        attack_record = net.attack_record # list of all attack initialisations


        pickle.dump(attack_record, f, pickle.HIGHEST_PROTOCOL) # save the attack


# The class of the adversary to implement
# The goal is to use the same episodes for all types attacks, therefore when capturing the
# attack we use only the constant attack

conAttack = hostClass.ConstantAttack
attackClasses = [conAttack] 

# network topologies to create evalution episodes for
commonMaps = [NetworkMediumVeryHard, NetworkMalialisTeamFull, NetworkMediumOptimal, NetworkFullTeamHard]

for common_map in commonMaps:
    common_map.drift = 0
    generateAttacks(common_map, attackClasses)


