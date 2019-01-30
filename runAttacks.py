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

adversarialLeaf = hostClass.adversarialLeaf


attackClasses = [conAttack, gradualIncrease, shortPulse, mediumPulse,
    largePulse ] 


# class GeneralSettingsObject(object):
#     # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
#     SaveModelEnum = Enum('SaveModel', 'neither save load')
#     debug = False
#     # save_attack = SaveAttackEnum.neither
#     save_model = SaveModelEnum.load

def run_attacks(assignedNetwork, assignedAgent, file_path, adversaryAttacker, prefix):

    load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
    network_emulator = network_new.network_full # network_quick # network_full
    assignedNetwork.emulator = network_emulator
    assignedNetwork.drift = 0 # we don't use drift in testing
    assignedAgent.save_model_mode = mapsAndSettings.defender_mode_enum.test_short

    for attackClass in attackClasses:
        print(attackClass.getName())
        genericAgent = mapsAndSettings.create_generic_dec(assignedAgent, assignedNetwork)
        
        attack_location = load_attack_path+attackClass.getName()+".apkl"

        exp = experiment.Experiment(attackClass, assignedNetwork, 
            assignedAgent, None, load_attack_path=attack_location)

        exp.run(prefix, genericAgent, file_path)
    if adversaryAttacker:
        adversaryAttacker.save_model_mode = mapsAndSettings.defender_mode_enum.test_short

        # attackClasses.insert(adversarialLeaf, 0)
        print("doing adversaryAttacker")
        attackClass = adversarialLeaf

        genericAgent = mapsAndSettings.create_generic_dec(assignedAgent, assignedNetwork)
        attack_location = load_attack_path+attackClass.getName()+".apkl"
        exp = experiment.Experiment(attackClass, assignedNetwork, 
            assignedAgent, adversaryAttacker, load_attack_path=attack_location)

        exp.run(prefix, genericAgent, file_path)

    mapsAndSettings.getSummary(attackClasses, file_path, assignedAgent, adversaryAttacker, prefix)




