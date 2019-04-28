import experiment
import mapsAndSettings
from enum import Enum
import network.network_new as network_new
import network.hosts as hostClass

import copy
"""
Rather than using runSARSA or runDDQN, have a master file that runs attacks for us

"""

# conAttack = hostClass.ConstantAttack
# shortPulse = hostClass.ShortPulse
# mediumPulse = hostClass.MediumPulse
# largePulse = hostClass.LargePulse
# gradualIncrease = hostClass.GradualIncrease

adversarialLeaf = hostClass.adversarialLeaf


attackers = [mapsAndSettings.adv_constant, mapsAndSettings.adv_pulse_short, mapsAndSettings.adv_pulse_medium, mapsAndSettings.adv_pulse_large,
    mapsAndSettings.adv_gradual, mapsAndSettings.adv_split] 

DEFAULT_NUMBER_ATTACKS = 100 # 100

# class GeneralSettingsObject(object):
#     # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
#     SaveModelEnum = Enum('SaveModel', 'neither save load')
#     debug = False
#     # save_attack = SaveAttackEnum.neither
#     save_model = SaveModelEnum.load

def run_attacks(assignedNetwork, assignedAgent, file_path, smart_attacker, prefix, custom_iterations_between_second = DEFAULT_NUMBER_ATTACKS):
    #assert(custom_iterations_between_second == DEFAULT_NUMBER_ATTACKS)



    load_attack_path = "attackSimulations/{0}/".format(assignedNetwork.name)
    network_emulator = network_new.network_full # network_quick # network_full
    assignedNetwork.emulator = network_emulator

    initial_save_mode = assignedAgent.save_model_mode

    assignedAgent.save_model_mode = mapsAndSettings.defender_mode_enum.test_short
    
    original_iterations = assignedNetwork.iterations_between_second

    attack_location = load_attack_path+"OneAndAQuarterAttack.apkl"
    # print(attack_location)
    
    attackClass = adversarialLeaf
    assignedNetwork.save_per_step_stats = True


    for attacker in attackers:
        # if attacker != mapsAndSettings.adv_pulse_short:
        #     continue
        assignedNetwork.iterations_between_second = custom_iterations_between_second
        print(attacker.name)
        print("\n\n\n")
        genericAgent = mapsAndSettings.create_generic_dec(assignedAgent, assignedNetwork)
        
        exp = experiment.Experiment(attackClass, assignedNetwork, 
            assignedAgent, attacker, load_attack_path=attack_location)       


        exp.run(prefix, genericAgent, file_path)
        assignedNetwork.iterations_between_second = original_iterations
    if smart_attacker and smart_attacker.is_intelligent:
        init_adv_save_model = smart_attacker.save_model_mode
        smart_attacker.save_model_mode = mapsAndSettings.defender_mode_enum.test_short

        # we've intentionally left the actions at standard rate to reflect training for advesary
        # attackClasses.insert(adversarialLeaf, 0)
        print("doing smart_attacker")
        assignedNetwork.iterations_between_second = custom_iterations_between_second
        genericAgent = mapsAndSettings.create_generic_dec(assignedAgent, assignedNetwork)
        #attack_location = load_attack_path+attackClass.getName()+".apkl"
        exp = experiment.Experiment(attackClass, assignedNetwork, 
            assignedAgent, smart_attacker, load_attack_path=attack_location)

        exp.run(prefix, genericAgent, file_path)
        smart_attacker.save_model_mode = init_adv_save_model
        attackers.append(smart_attacker)

        assignedNetwork.iterations_between_second = original_iterations
    
    mapsAndSettings.getSummary(attackers, file_path, assignedAgent, prefix)
    if smart_attacker and smart_attacker.is_intelligent:
        attackers.remove(smart_attacker)
    #undo changes

    assignedAgent.save_model_mode = initial_save_mode
    assignedNetwork.save_per_step_stats = False






