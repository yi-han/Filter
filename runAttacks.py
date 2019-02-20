import experiment
import mapsAndSettings
from enum import Enum
import network.network_new as network_new
import network.hosts as hostClass

import copy
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

    network = copy.deepcopy(assignedNetwork)
    agent = copy.deepcopy(assignedAgent)


    load_attack_path = "attackSimulations/{0}/".format(network.name)
    network_emulator = network_new.network_full # network_quick # network_full
    network.emulator = network_emulator

    initial_save_mode = agent.save_model_mode
    initial_drift = network.drift

    network.drift = 0 # we don't use drift in testing
    agent.save_model_mode = mapsAndSettings.defender_mode_enum.test_short
    
    original_iterations = assignedNetwork.iterations_between_action



    for attackClass in attackClasses:
        assignedNetwork.iterations_between_action = 200
        print(attackClass.getName())
        genericAgent = mapsAndSettings.create_generic_dec(agent, network)
        
        attack_location = load_attack_path+"genericAttack.apkl"

        exp = experiment.Experiment(attackClass, network, 
            agent, None, load_attack_path=attack_location)

        exp.run(prefix, genericAgent, file_path)
        assignedNetwork.iterations_between_action = original_iterations
    if adversaryAttacker:
        init_adv_save_model = adversaryAttacker.save_model_mode
        adversaryAttacker.save_model_mode = mapsAndSettings.defender_mode_enum.test_short

        
        # attackClasses.insert(adversarialLeaf, 0)
        print("doing adversaryAttacker")
        attackClass = adversarialLeaf

        genericAgent = mapsAndSettings.create_generic_dec(agent, network)
        attack_location = load_attack_path+attackClass.getName()+".apkl"
        exp = experiment.Experiment(attackClass, network, 
            agent, adversaryAttacker, load_attack_path=attack_location)

        exp.run(prefix, genericAgent, file_path)
        adversaryAttacker.save_model_mode = init_adv_save_model
        attackClasses.append(adversarialLeaf)
    mapsAndSettings.getSummary(attackClasses, file_path, agent, adversaryAttacker, prefix)
    if adversaryAttacker:
        attackClasses.remove(adversarialLeaf)
    #undo changes

    network.drift = initial_drift
    agent.save_model_mode = initial_save_mode





