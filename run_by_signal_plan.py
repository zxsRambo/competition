import engine

interval = 1.0                          # seconds of each step
threadNum = 1                           # this .so is single thread version, this parameter is useless
saveReplay = True                       # set to True if your want to replay the traffic in GUI
rlTrafficLight = True                   # set to True to control the signal
changeLane = False                      # set to False if changing lane is not considered
roadnetFile = "data/roadnet/roadnet_uniform_200.json"
flowFile = "data/flow/flow_uniform_200.json"
planFile = "data/plan/signal_plan.txt"
num_step = 3600

eng = engine.Engine(interval, threadNum, saveReplay, rlTrafficLight, changeLane)
eng.load_roadnet(roadnetFile)
eng.load_flow(flowFile)

plan = open(planFile)
plan.readline()

for step in range(num_step):
    phase = int(plan.readline())
    eng.set_tl_phase("intersection_1_1", phase)  # set traffic light of intersection_1_1 to phase (phases of intersection is defined in roadnetFile)
    eng.next_step()

    current_time = eng.get_current_time()                      # return a double, time past in seconds
    lane_vehicle_count = eng.get_lane_vehicle_count()                # return a dict, {lane_id: lane_count, ...}
    lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()        # return a dict, {lane_id: lane_waiting_count, ...}
    lane_vehicles = eng.get_lane_vehicles()                     # return a dict, {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
    vehicle_speed = eng.get_vehicle_speed()                     # return a dict, {vehicle_id: vehicle_speed, ...}
    vehicle_distance = eng.get_vehicle_distance()                  # return a dict, {vehicle_id: vehicle_distance, ...}

    print("Time: {}, Phase: {}, lane_vehicle_count: {}".format(current_time, phase, lane_vehicle_count))