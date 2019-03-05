'''
@time: 2019/04/27
@description: apply a reinforcement learning algorithm to traffic signal
'''

from cityflow_env import CityFlowEnv
from agent import DQNAgent
from utility import parse_roadnet
import numpy as np
import os

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

    os.environ["CUDA_VISIBLE_DEVICES"] = ''

    config['lane_phase_info'] = parse_roadnet(config['roadnet']) # get lane and phase information by parsing the roadnet
    intersection_id = list(config['lane_phase_info'].keys())[0]
    phase_list = config['lane_phase_info'][intersection_id]['phase']
    config['state_size'] = len(config['lane_phase_info'][intersection_id]['start_lane']) + 1
    config['action_size'] = len(phase_list)

    env = CityFlowEnv(config)
    agent = DQNAgent(config)

    # reset initially
    state = env.reset()

    done = False
    batch_size = 32
    EPISODES = 100
    HORIZON = 3600
    state_size = config['state_size']

    for e in range(EPISODES):
        state = env.reset()
        state = np.array(list(state['start_lane_vehicle_count'].values()) + [state['current_phase']]) # a sample state representation
        state = np.reshape(state, [1, state_size])
        done = False
        last_action = phase_list[agent.choose_action(state)]
        while not done:
            action = agent.choose_action(state)
            action = phase_list[action]
            env.step(action)

            next_state = env.get_state()
            reward = env.get_reward()
            done = env.is_done()

            print("time: {}, phase: {}, current phase time: {}, action: {}".format(next_state['current_time'],
                                                                                   next_state['current_phase'],
                                                                                   next_state["current_phase_time"],
                                                                                   action))

            next_state = np.array(list(next_state['start_lane_vehicle_count'].values()) + [next_state['current_phase']])
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

        if e % 10 == 0:
            agent.save("model/trafficLight-dqn.h5")

    # log environment files
    env.log()