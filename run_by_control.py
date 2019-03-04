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
        'roadnet': 'data/roadnet/roadnet_uniform_600.json',
        'flow': 'data/flow/flow_uniform_600.json',
        'phase_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'replay_data_path': 'data/frontend/web',
        'records_path': 'records',
        'horizon': 3600

    }

    config['lane_phase_info'] = parse_roadnet(config['roadnet']) # get lane and phase information by parsing the roadnet

    env = CityFlowEnv(config)
    agent = SOTLAgent(config)

    # reset initially
    state, _, done = env.reset()

    while not done:
        action = agent.choose_action(state)
        state, _, done = env.step(action)

    # log environment files
    env.log()