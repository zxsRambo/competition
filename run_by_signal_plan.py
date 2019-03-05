import engine
from sim_setting import sim_setting_control

roadnetFile = "data/uniform_200/roadnet.json"
flowFile = "data/uniform_200/flow.json"
planFile = "data/uniform_200/signal_plan.txt"
num_step = 3600

eng = engine.Engine(sim_setting_control["interval"],
                    sim_setting_control["threadNum"],
                    sim_setting_control["saveReplay"],
                    sim_setting_control["rlTrafficLight"],
                    sim_setting_control["changeLane"])
eng.load_roadnet(roadnetFile)
eng.load_flow(flowFile)

plan = open(planFile)
plan.readline()

for step in range(num_step):
    current_time = eng.get_current_time()                      # return a double, time past in seconds
    lane_vehicle_count = eng.get_lane_vehicle_count()                # return a dict, {lane_id: lane_count, ...}
    lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()        # return a dict, {lane_id: lane_waiting_count, ...}
    lane_vehicles = eng.get_lane_vehicles()                     # return a dict, {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
    vehicle_speed = eng.get_vehicle_speed()                     # return a dict, {vehicle_id: vehicle_speed, ...}
    vehicle_distance = eng.get_vehicle_distance()                  # return a dict, {vehicle_id: vehicle_distance, ...}

    phase = int(plan.readline())
    eng.set_tl_phase("intersection_1_1", phase)  # set traffic light of intersection_1_1 to phase (phases of intersection is defined in roadnetFile)
    eng.next_step()

    print("Time: {}, Phase: {}, lane_vehicle_count: {}".format(current_time, phase, lane_vehicle_count))