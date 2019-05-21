"""
Generate and run attacks

"""

"""
Attacks to be saved in list of lists of what generated, allow the network to
decide how to respond
"""
import sys
import os#, sys, logging
import network.network_new as netModule

import network.hosts as hostClass
import os#, sys, logging
import pickle
from mapsAndSettings import *


def generateAttacks(networkSettings, attackClasses, max_epLength = -1, num_episodes = 500):
    path = "attackSimulations/{0}/".format(networkSettings.name)
    # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    # save_attack = SaveAttackEnum.save
    
    reward_overload = -1

    networkSettings.is_sig_attack = True # ensure we only have significant attacks
    if not os.path.exists(path):
        os.makedirs(path)
    # for attackClass in attackClasses:
        # print(attackClass)
    attack_path = path+"OneAndAQuarterAttack.apkl"
    # attack_path = path+"OnePointTwo.apkl"
    # just do it once 
    with open(attack_path, "wb") as f:
        
        # run all the simulations
        net = netModule.network_full(networkSettings, conAttack, AimdMalialis, None, None, True)
        for _ in range(num_episodes):
            net.reset()

        attack_record = net.attack_record # list of all attack initialisations


        pickle.dump(attack_record, f, pickle.HIGHEST_PROTOCOL)


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack

adversarialLeaf = hostClass.adversarialLeaf

attackClasses = [conAttack] 

# commonMaps = [NetworkMalialisSmall, NetworkSingleTeamMalialisMedium, NetworkSixFour, NetworkMalialisTeamFull, NetworkSixHard, NetworkMediumVeryHard, NetworkMalialisTeamFull, NetworkMediumOptimal, NetworkFullTeamHard]
commonMaps = [NetworkMediumVeryHard, NetworkMalialisTeamFull, NetworkMediumOptimal, NetworkFullTeamHard]
for common_map in commonMaps:
    common_map.drift = 0
    print(common_map)
    generateAttacks(common_map, attackClasses)


