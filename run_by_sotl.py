'''
@time: 2019/04/27
@description: apply a control algorithm to traffic signal
'''

from cityflow_env import CityFlowEnv
from agent import SOTLAgent
from utility import parse_roadnet

if __name__ == "__main__":
    ## configuration for both environment and agent
    config = {
        'roadnet': 'data/uniform_600/roadnet.json',
        'flow': 'data/uniform_600/flow.json',
        'phase_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'replay_data_path': 'data/frontend/web',
        'records_path': 'records',
        'horizon': 3600

    }

    config['lane_phase_info'] = parse_roadnet(config['roadnet']) # get lane and phase information by parsing the roadnet

    env = CityFlowEnv(config)
    agent = SOTLAgent(config)

    # reset initially
    state = env.reset()
    last_action = agent.choose_action(state)
    done = False
    while not done:
        action = agent.choose_action(state)
        if last_action != action:
            for i in range(5):
                env.step(0)
            last_action = action
        env.step(action)
        state = env.get_state()
        done = env.is_done()

        print("time: {}, phase: {}, current phase time: {}, action: {}".format(state['current_time'], state['current_phase'],
                                                                               state["current_phase_time"],
                                                                               action))
    # log environment files
    env.log()