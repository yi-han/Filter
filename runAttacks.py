import experiment
import mapsAndSettings
from enum import Enum
import network.network_new as network_new
import network.hosts as hostClass
"""
Rather than using runSARSA or runDDQN, have a master file that runs attacks for us

"""

conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease] 


class GeneralSettingsObject(object):
    # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
    SaveModelEnum = Enum('SaveModel', 'neither save load')
    debug = False
    # save_attack = SaveAttackEnum.neither
    save_model = SaveModelEnum.load

def run_attacks(genericAgent, twist, assignedNetwork, assignedAgent):

    load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
    network_emulator = network_new.network_full # network_quick # network_full
    assignedNetwork.emulator = network_emulator

    for attackClass in attackClasses:
        attack_location = load_attack_path+attackClass.getName()+".apkl"

        exp = experiment.Experiment(attackClass, GeneralSettingsObject, assignedNetwork, 
            assignedAgent, twist=twist, load_attack_path=attack_location)

        exp.run(0, genericAgent)
    mapsAndSettings.getSummary(attackClasses, exp.load_path, assignedAgent)




