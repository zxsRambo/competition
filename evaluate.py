import engine
import json
import pandas as pd
import numpy as np

def main():

    dic_sim_setting = {
        "interval": 1.0,                          # seconds of each step
        "threadNum": 1,                           # this .so is single thread version, this parameter is useless
        "saveReplay": True,                       # set to True if your want to replay the traffic in GUI
        "rlTrafficLight": True,                   # set to True to control the signal
        "changeLane": False,                      # set to False if changing lane is not considered
        "num_step": 3600}

    list_traffic_memo = ["uniform_200"]

    for memo in list_traffic_memo:
        evaluate_one_traffic(dic_sim_setting, memo)

def evaluate_one_traffic(dic_sim_setting, memo):

    roadnetFile = "data/roadnet/roadnet_{0}.json".format(memo)
    flowFile = "data/flow/flow_{0}.json".format(memo)
    planFile = "data/plan/signal_plan_{0}.txt".format(memo)
    outFile = "data/evaluation/evaluation_{0}.txt".format(memo)

    df_vehicle_actual_enter_leave = test_run(dic_sim_setting, roadnetFile, flowFile, planFile)
    df_vehicle_planed_enter = get_planed_entering(flowFile, dic_sim_setting)
    # add planed entering to actual leaving
    tt = cal_travel_time(df_vehicle_actual_enter_leave, df_vehicle_planed_enter, outFile, dic_sim_setting)
    print("====================== travel time ======================")
    print("{0}: {1:.2f} s".format(memo, tt))
    print("====================== travel time ======================")


def test_run(dic_sim_setting, roadnetFile, flowFile, planFile):


    eng = engine.Engine(dic_sim_setting["interval"], dic_sim_setting["threadNum"],
                        dic_sim_setting["saveReplay"], dic_sim_setting["rlTrafficLight"],
                        dic_sim_setting["changeLane"])
    eng.load_roadnet(roadnetFile)
    eng.load_flow(flowFile)

    plan = open(planFile, "r")
    plan.readline()

    # get lanes todo--need to be changed when lane setting or intersection setting is changed
    inter_name = "intersection_1_1"
    list_all_lanes = list(eng.get_lane_vehicles().keys())
    dic_roadnet = json.load(open(roadnetFile, "r"))
    dic_intersections = {}
    for inter in dic_roadnet["intersections"]:
        dic_intersections[inter["id"]] = inter
    list_exiting_lanes = []
    list_non_exiting_lanes = []
    for lane in list_all_lanes:
        int_x, int_y, direc, l_id = list(map(int, lane.split('_')[1:]))
        if direc == 0:
            int_x_end = int_x + 1
            int_y_end = int_y
        elif direc == 1:
            int_x_end = int_x
            int_y_end = int_y + 1
        elif direc == 2:
            int_x_end = int_x - 1
            int_y_end = int_y
        elif direc == 3:
            int_x_end = int_x
            int_y_end = int_y - 1
        if dic_intersections["intersection_{0}_{1}".format(int_x_end, int_y_end)]["virtual"]:
            list_exiting_lanes.append(lane)
        else:
            list_non_exiting_lanes.append(lane)

    # maintain list of vehicles in exiting lanes and non-exiting lanes
    list_non_exiting_lane_vehicles_prev = []
    dic_vehicle_enter_leave_time = {}

    for step in range(dic_sim_setting["num_step"]):

        current_time = eng.get_current_time()  # return a double, time past in seconds
        lane_vehicles = eng.get_lane_vehicles()  # return a dict, {lane_id: [vehicle1_id, vehicle2_id, ...], ...}

        list_non_exiting_lane_vehicles_cur = []
        for lane in list_non_exiting_lanes:
            list_non_exiting_lane_vehicles_cur += lane_vehicles[lane]
        for vec in (set(list_non_exiting_lane_vehicles_cur) - set(list_non_exiting_lane_vehicles_prev)):
            # new entering vehicles
            dic_vehicle_enter_leave_time[vec] = {"enter_time": current_time-1, "leave_time": float("nan")}
        for vec in (set(list_non_exiting_lane_vehicles_prev) - set(list_non_exiting_lane_vehicles_cur)):
            # new left vehicles
            dic_vehicle_enter_leave_time[vec]["leave_time"] = current_time-1

        if current_time % 100 == 0:
            print("Time: {} / {}".format(current_time, dic_sim_setting["num_step"]))

        phase = int(plan.readline())
        eng.set_tl_phase(inter_name, phase)  # set traffic light of intersection_1_1 to phase (phases of intersection is defined in roadnetFile)
        eng.next_step()

        list_non_exiting_lane_vehicles_prev = list_non_exiting_lane_vehicles_cur[:]

    df_vehicle_enter_leave = pd.DataFrame(dic_vehicle_enter_leave_time).transpose()
    assert np.all((df_vehicle_enter_leave["enter_time"] >= 0).values)
    return df_vehicle_enter_leave


def get_planed_entering(flowFile, dic_sim_setting):
    # todo--check with huichu about how each vehicle is inserted, according to the interval. 1s error may occur.
    list_flow = json.load(open(flowFile, "r"))
    dic_traj = {}
    for flow_id, flow in enumerate(list_flow):
        step = 0
        list_ts_this_flow = []
        for step in range(dic_sim_setting["num_step"]):
            if step == 0:
                list_ts_this_flow.append(step)
            elif step - list_ts_this_flow[-1] >= flow["interval"]:
                list_ts_this_flow.append(step)

        for vec_id, ts in enumerate(list_ts_this_flow):
            dic_traj["flow_{0}_{1}".format(flow_id, vec_id)] = {"planed_enter_time": ts}

    return pd.DataFrame(dic_traj).transpose()

def cal_travel_time(df_vehicle_actual_enter_leave, df_vehicle_planed_enter, outFile, dic_sim_setting):

    df_res = pd.concat([df_vehicle_planed_enter, df_vehicle_actual_enter_leave], axis=1)
    assert len(df_res) == len(df_vehicle_planed_enter)

    df_res["leave_time"].fillna(dic_sim_setting["num_step"])
    df_res["travel_time"] = df_res["leave_time"] - df_res["planed_enter_time"]

    return df_res["travel_time"].mean()

main()