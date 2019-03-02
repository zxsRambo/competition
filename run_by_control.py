'''
@time: 2019/04/27
@description: main script to run the sample code
'''

import engine
import json
from cityflow_env import CityFlowEnv
from agent import SOTLAgent


def parse_roadnet(roadnetFile):
    roadnet = json.load(open(roadnetFile))
    lane_phase_info_dict ={}

    # many intersections exist in the roadnet and virtual intersection is controlled by signal
    for intersection in roadnet["intersections"]:
        if intersection['virtual']:
            continue
        lane_phase_info_dict[intersection['id']] = {"start_lane": [],
                                                     "end_lane": [],
                                                     "phase": [],
                                                     "phase_startLane_mapping": {},
                                                     "phase_roadLink_mapping": {}}
        road_links = intersection["roadLinks"]


        start_lane = []
        end_lane = []
        roadLink_lane_pair = {ri: [] for ri in
                              range(len(road_links))}  # roadLink includes some lane_pair: (start_lane, end_lane)

        for ri in range(len(road_links)):
            road_link = road_links[ri]
            for lane_link in road_link["laneLinks"]:
                sl = road_link['startRoad'] + "_" + str(lane_link["startLaneIndex"])
                el = road_link['endRoad'] + "_" + str(lane_link["endLaneIndex"])
                start_lane.append(sl)
                end_lane.append(el)
                roadLink_lane_pair[ri].append((sl, el))

        lane_phase_info_dict[intersection['id']]["start_lane"] = sorted(list(set(start_lane)))
        lane_phase_info_dict[intersection['id']]["end_lane"] = sorted(list(set(end_lane)))

        for phase_i in range(1, len(intersection["trafficLight"]["lightphases"])):
            p = intersection["trafficLight"]["lightphases"][phase_i]
            lane_pair = []
            start_lane = []
            for ri in p["availableRoadLinks"]:
                lane_pair.extend(roadLink_lane_pair[ri])
                if roadLink_lane_pair[ri][0][0] not in start_lane:
                    start_lane.append(roadLink_lane_pair[ri][0][0])
            lane_phase_info_dict[intersection['id']]["phase"].append(phase_i)
            lane_phase_info_dict[intersection['id']]["phase_startLane_mapping"][phase_i] = start_lane
            lane_phase_info_dict[intersection['id']]["phase_roadLink_mapping"][phase_i] = lane_pair

    return lane_phase_info_dict

if __name__ == "__main__":
    ## configuration for both environment and agent
    config = {
        'roadnet': 'data/roadnet/roadnet_uniform_600.json',
        'flow': 'data/flow/flow_uniform_600.json',
        'phase_list': [1, 2, 3, 4, 5, 6, 7, 8],
        'replay_data_path': 'data/frontend/web',
        'records_path': 'records'

    }

    config['lane_phase_info'] = parse_roadnet(config['roadnet']) # get lane and phase information by parsing the roadnet

    env = CityFlowEnv(config)
    agent = SOTLAgent(config)

    # reset initially
    state = env.reset()

    for step in range(3600):
        action = agent.choose_action(state)
        state = env.step(action)

    # log environment files
    env.log()