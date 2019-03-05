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
        'data': 'data/uniform_400',
        'roadnet': 'data/uniform_400/roadnet.json',
        'flow': 'data/uniform_400/flow.json',
        'phase_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'replay_data_path': 'data/frontend/web',
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

    batch_size = 32
    EPISODES = 100
    learning_start = 300
    update_model_freq = 300
    update_target_model_freq = 1500
    horizon = config['horizon']
    state_size = config['state_size']

    for e in range(EPISODES):
        # reset initially at each episode
        env.reset()
        t = 0
        state = env.get_state()
        state = np.array(list(state['start_lane_vehicle_count'].values()) + [state['current_phase']]) # a sample state definition
        state = np.reshape(state, [1, state_size])
        last_action = agent.choose_action(state)
        last_action = phase_list[last_action]
        while t < horizon:
            action = agent.choose_action(state)
            action = phase_list[action]
            if action == last_action:
                env.step(action)
            else:
                for _ in range(env.yellow_time):
                    env.step(0)  # required yellow time
                    t += 1
                    flag = (t >= horizon)
                    if flag:
                        break
                if flag:
                    break
                env.step(action)
            last_action = action
            t += 1
            next_state = env.get_state()
            reward = env.get_reward()
            next_state = np.array(list(next_state['start_lane_vehicle_count'].values()) + [next_state['current_phase']])
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state)
            state = next_state

            total_time = t + e * horizon
            if total_time > learning_start and total_time % update_model_freq == update_model_freq - 1:
                agent.replay()
            if total_time > learning_start and total_time % update_target_model_freq == update_target_model_freq -1:
                agent.update_target_network()

            print("episode: {}/{}, time: {}, acton: {}, reward: {}"
                  .format(e, EPISODES, t-1, action, reward))

        if e % 10 == 0:
            if not os.path.exists("model"):
                os.makedirs("model")
            agent.save("model/trafficLight-dqn-{}.h5".format(e))

    # log environment files
    env.log()