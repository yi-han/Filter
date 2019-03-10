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
    mapsAndSettings.adv_gradual, mapsAndSettings.adv_split ] 

DEFAULT_NUMBER_ATTACKS = 200

# class GeneralSettingsObject(object):
#     # SaveAttackEnum = Enum('SaveAttack', 'neither save load')
#     SaveModelEnum = Enum('SaveModel', 'neither save load')
#     debug = False
#     # save_attack = SaveAttackEnum.neither
#     save_model = SaveModelEnum.load

def run_attacks(assignedNetwork, assignedAgent, file_path, smart_attacker, prefix, custom_iterations_between_action = DEFAULT_NUMBER_ATTACKS):
    assert(custom_iterations_between_action == DEFAULT_NUMBER_ATTACKS)
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

    attack_location = load_attack_path+"onePerAttack.apkl"
    print(attack_location)
    
    attackClass = adversarialLeaf


    for attacker in attackers:
        assignedNetwork.iterations_between_action = custom_iterations_between_action
        print(attacker.name)
        print("\n\n\n")
        genericAgent = mapsAndSettings.create_generic_dec(agent, network)
        
        exp = experiment.Experiment(attackClass, network, 
            agent, attacker, load_attack_path=attack_location)       


        exp.run(prefix, genericAgent, file_path)
        assignedNetwork.iterations_between_action = original_iterations
    if smart_attacker and smart_attacker.is_intelligent:
        init_adv_save_model = smart_attacker.save_model_mode
        smart_attacker.save_model_mode = mapsAndSettings.defender_mode_enum.test_short

        # we've intentionally left the actions at standard rate to reflect training for advesary
        # attackClasses.insert(adversarialLeaf, 0)
        print("doing smart_attacker")
        assignedNetwork.iterations_between_action = custom_iterations_between_action
        genericAgent = mapsAndSettings.create_generic_dec(agent, network)
        #attack_location = load_attack_path+attackClass.getName()+".apkl"
        exp = experiment.Experiment(attackClass, network, 
            agent, smart_attacker, load_attack_path=attack_location)

        exp.run(prefix, genericAgent, file_path)
        smart_attacker.save_model_mode = init_adv_save_model
        attackers.append(smart_attacker)

        assignedNetwork.iterations_between_action = original_iterations
    
    mapsAndSettings.getSummary(attackers, file_path, agent, prefix)
    if smart_attacker:
        attackers.remove(smart_attacker)
    #undo changes

    network.drift = initial_drift
    agent.save_model_mode = initial_save_mode





