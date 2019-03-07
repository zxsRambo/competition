'''
@time: 2019/04/27
@description: apply a control algorithm to traffic signal
'''

from cityflow_env import CityFlowEnv
from agent import SOTLAgent
from utility import parse_roadnet
import argparse

if __name__ == "__main__":
    ## configuration for both environment and agent
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=int, default=0)     
    args = parser.parse_args()
    config = {
        'scenario': args.scenario,
        'data': 'data/scenario_{}'.format(args.scenario),
        'roadnet': 'data/scenario_{}/roadnet.json'.format(args.scenario),
        'flow': 'data/scenario_{}/flow.json'.format(args.scenario),
        'phase_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'replay_data_path': 'data/frontend/web',
        'horizon': 3600

    }

    config['lane_phase_info'] = parse_roadnet(config['roadnet'])  # get lane and phase mapping by parsing the roadnet

    env = CityFlowEnv(config)
    agent = SOTLAgent(config)

    # reset initially
    t = 0
    env.reset()
    last_action = agent.choose_action(env.get_state())

    while t < config['horizon']:
        state = env.get_state()
        action = agent.choose_action(state)
        if action == last_action:
            env.step(action)
        else:
            for _ in range(env.yellow_time):
                env.step(0)  # required yellow time
                t += 1
                flag = (t >= config['horizon'])
                if flag:
                    break
            if flag:
                break
            env.step(action)
        last_action = action
        t += 1
        print("time: {}, current phase: {}, current phase time: {}".format(state['current_time'], state['current_phase'],
                                                                           state['current_phase_time']))

    # log environment files
    env.log()