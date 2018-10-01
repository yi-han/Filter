import math
import agent.genericDecentralised as genericDecentralised



def create_generic_dec(gs, general_s, ns):
    """
    gs = generic_settings, ns = network_settings

    """
    throttlers_not_allocated = ns.N_state
    group_size = gs.group_size
    sub_agent = gs.sub_agent
    num_teams = math.ceil(ns.N_state/group_size)

    sub_agent_list = []

    test = (general_s.save_model is general_s.SaveModelEnum.test)
    print(sub_agent)
    while throttlers_not_allocated > 0:
        print("currently {0} throttlers_not_allocated".format(throttlers_not_allocated))
        agent_to_allocate = min(throttlers_not_allocated, group_size)
        sub_agent_list.append(sub_agent(ns.action_per_throttler**agent_to_allocate, gs.pre_train_steps,
            ns.action_per_throttler, agent_to_allocate, gs.tau, gs.y, general_s.debug,
            test))
        throttlers_not_allocated -= agent_to_allocate

    #print("\nTest {0} \n".format(sub_agent_list[0].N_action))
    master = genericDecentralised.AgentOfAgents(
        ns.N_action, gs.pre_train_steps, ns.action_per_throttler, ns.N_state,
            sub_agent_list, gs.tau, gs.y, general_s.debug, 
            test
        )
    return master


