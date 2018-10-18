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


def generateAttacks(networkSettings, attackClasses, max_epLength = 60, num_episodes = 100):
    path = "attackSimulations/{0}/".format(networkSettings.name)
    # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    # save_attack = SaveAttackEnum.save
    
    reward_overload = -1


    if not os.path.exists(path):
        os.makedirs(path)
    for attackClass in attackClasses:
        attack_path = path+attackClass.getName()+".apkl"
        
        with open(attack_path, "wb") as f:
            
            # run all the simulations
            net = netModule.network(networkSettings, reward_overload, attackClass, max_epLength, None, True)
            for _ in range(num_episodes):
                net.reset()

            attack_record = net.attack_record # list of all attack initialisations


            pickle.dump(attack_record, f, pickle.HIGHEST_PROTOCOL)


# The class of the adversary to implement
conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 

generateAttacks(NetworkSingleTeamMalialisMedium, attackClasses)