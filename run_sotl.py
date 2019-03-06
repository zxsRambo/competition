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
        'data': 'data/uniform_200',
        'roadnet': 'data/uniform_200/roadnet.json',
        'flow': 'data/uniform_200/flow.json',
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