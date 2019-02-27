import engine

class CityFlowEnv():
    ''' Simulator Environment with CityFlow
    '''
    def __init__(self, config):
        self.eng = engine.Engine(1, 1, True, True, False)
        self.eng.load_roadnet(config['roadnet'])
        self.eng.load_flow(config['flow'])
        self.config = config

    def reset(self):
        self.eng.reset()
        return self.get_state()

    def step(self, action):
        self.eng.set_tl_phase("intersection_1_1", action)
        self.eng.next_step()
        return self.get_state()

    def get_state(self):
        state = {}
        state['lane_vehicle_count'] = self.eng.get_lane_vehicle_count()  # {lane_id: lane_count, ...}
        state['lane_waiting_vehicle_count'] = self.eng.get_lane_waiting_vehicle_count()  # {lane_id: lane_waiting_count, ...}
        state['lane_vehicles'] = self.eng.get_lane_vehicles()  # {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
        state['vehicle_speed'] = self.eng.get_vehicle_speed()  # {vehicle_id: vehicle_speed, ...}
        state['vehicle_distance'] = self.eng.get_vehicle_distance() # {vehicle_id: distance, ...}
        state['current_time'] = self.eng.get_current_time()
        return state

    def log(self):
        self.eng.print_log(self.config['replay_data_path'] + "/replay_roadnet.json",
                           self.config['replay_data_path'] + "/replay_flow.json")