import engine
import pandas as pd
import os

class CityFlowEnv():
    ''' Simulator Environment with CityFlow
    '''
    def __init__(self, config):
        self.eng = engine.Engine(1, 1, True, True, False)
        self.eng.load_roadnet(config['roadnet'])
        self.eng.load_flow(config['flow'])
        self.config = config
        self.horizon = config['horizon']
        self.lane_phase_info = config['lane_phase_info'] # "intersection_1_1"

        self.intersection_id = list(self.lane_phase_info.keys())[0]
        self.start_lane = self.lane_phase_info[self.intersection_id]['start_lane']
        self.phase_list = self.lane_phase_info[self.intersection_id]["phase"]
        self.phase_startLane_mapping = self.lane_phase_info[self.intersection_id]["phase_startLane_mapping"]

        self.current_phase = self.phase_list[0]
        self.current_phase_time = 0
        self.yellow_time = 5

        self.phase_log = []


    def reset(self):
        self.eng.reset()
        return self.get_state(), self.get_reward(), self.is_done()

    def step(self, action):

        if self.current_phase != action:
            if action == 0:
                self.current_phase = action               # yellow light is manually set from signal plan file
                self.current_phase_time = 1
            else:
                for i in range(self.yellow_time):         # yellow light is automatically set when changing lights
                    self.eng.set_tl_phase(self.intersection_id, 0)
                    self.eng.next_step()
                    self.phase_log.append(0)
                self.current_phase = action
                self.current_phase_time = 1
        else:
            self.current_phase_time += 1

        self.eng.set_tl_phase("intersection_1_1", self.current_phase)
        self.eng.next_step()
        self.phase_log.append(self.current_phase)

        return self.get_state(), self.get_reward(), self.is_done()

    def get_state(self):
        state = {}
        state['lane_vehicle_count'] = self.eng.get_lane_vehicle_count()  # {lane_id: lane_count, ...}
        state['start_lane_vehicle_count'] = {lane: self.eng.get_lane_vehicle_count()[lane] for lane in self.start_lane}
        state['lane_waiting_vehicle_count'] = self.eng.get_lane_waiting_vehicle_count()  # {lane_id: lane_waiting_count, ...}
        state['lane_vehicles'] = self.eng.get_lane_vehicles()  # {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
        state['vehicle_speed'] = self.eng.get_vehicle_speed()  # {vehicle_id: vehicle_speed, ...}
        state['vehicle_distance'] = self.eng.get_vehicle_distance() # {vehicle_id: distance, ...}
        state['current_time'] = self.eng.get_current_time()
        state['current_phase'] = self.current_phase
        state['current_phase_time'] = self.current_phase_time

        return state

    def get_reward(self):
        # a sample reward function which calculates the total of waiting vehicles
        lane_waiting_vehicle_count = self.eng.get_lane_waiting_vehicle_count()
        reward = -1 * sum(list(lane_waiting_vehicle_count.values()))
        return reward

    def is_done(self):
        # a sample condition to terminate this episode if number of waiting vehicle exceed the threshold.
        start_lane_waiting_vehicle_count = {lane: self.eng.get_lane_waiting_vehicle_count()[lane] for lane in self.start_lane}
        if sum(list(start_lane_waiting_vehicle_count.values())) >= 200:
            return True
        else:
            return False

    def log(self):
        self.eng.print_log(self.config['replay_data_path'] + "/replay_roadnet.json",
                           self.config['replay_data_path'] + "/replay_flow.json")
        df = pd.DataFrame({'phase': self.phase_log})
        df.to_csv(os.path.join(self.config['records_path'], 'signal_plan.txt'), index=None)