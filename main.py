'''
@time: 2019/04/27
@licese: (C) Copyright 2019-2020, Shanghai Tianrang Intelligent Technology Corporation Limited.
'''
import engine
from cityflow_env import CityFlowEnv
from agent import FixedtimeAgent

if __name__ == "__main__":
    ## configuration for both environment and agent
    config = {
        'roadnet': 'data/roadnet/roadnet_1_1.json',
        'flow': 'data/flow/uniform_400.json',
        'phase_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'replay_data_path': 'data/frontend/web',
        'records_path': 'records'

    }

    env = CityFlowEnv(config)
    agent = FixedtimeAgent(config)

    # reset initially
    state = env.reset()

    for step in range(3600):
        action = agent.choose_action(state)
        state = env.step(action)

    # log environment and agent files
    env.log()
    agent.log()