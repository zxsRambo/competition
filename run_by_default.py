import engine

interval = 1.0                          # seconds of each step
threadNum = 1                           # this .so is single thread version, this parameter is useless
saveReplay = True                       # set to True if your want to replay the traffic in GUI
rlTrafficLight = False                  # set to False to control the signal by default
changeLane = False                      # set to False if changing lane is not considered
roadnetFile = 'data/uniform_600/roadnet.json'
flowFile = 'data/uniform_600/flow.json'
num_step = 3600

eng = engine.Engine(interval, threadNum, saveReplay, rlTrafficLight, changeLane)
eng.load_roadnet(roadnetFile)
eng.load_flow(flowFile)

for step in range(num_step):
    eng.next_step()
    current_time = eng.get_current_time()                      # return a double, time past in seconds
    lane_vehicle_count = eng.get_lane_vehicle_count()                # return a dict, {lane_id: lane_count, ...}
    lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()        # return a dict, {lane_id: lane_waiting_count, ...}
    lane_vehicles = eng.get_lane_vehicles()                     # return a dict, {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
    vehicle_speed = eng.get_vehicle_speed()                     # return a dict, {vehicle_id: vehicle_speed, ...}
    vehicle_distance = eng.get_vehicle_distance()                  # return a dict, {vehicle_id: vehicle_distance, ...}

    print("Time: {}, lane_vehicle_count: {}".format(current_time, lane_vehicle_count))