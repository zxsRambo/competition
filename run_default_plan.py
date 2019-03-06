import engine
from sim_setting import sim_setting_default

num_step = 3600

eng = engine.Engine(sim_setting_default["interval"],
                    sim_setting_default["threadNum"],
                    sim_setting_default["saveReplay"],
                    sim_setting_default["rlTrafficLight"],
                    sim_setting_default["changeLane"])
roadnetFile = "data/uniform_200/roadnet.json"
flowFile = "data/uniform_200/flow.json"
eng.load_roadnet(roadnetFile)
eng.load_flow(flowFile)

for step in range(num_step):
    current_time = eng.get_current_time()                      # return a double, time past in seconds
    lane_vehicle_count = eng.get_lane_vehicle_count()                # return a dict, {lane_id: lane_count, ...}
    lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()        # return a dict, {lane_id: lane_waiting_count, ...}
    lane_vehicles = eng.get_lane_vehicles()                     # return a dict, {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
    vehicle_speed = eng.get_vehicle_speed()                     # return a dict, {vehicle_id: vehicle_speed, ...}
    vehicle_distance = eng.get_vehicle_distance()                  # return a dict, {vehicle_id: vehicle_distance, ...}
    eng.next_step()

    print("Time: {}, lane_vehicle_count: {}".format(current_time, lane_vehicle_count))