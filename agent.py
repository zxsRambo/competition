import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class SOTLAgent():
    ''' Agent using Fixed-time algorithm to control traffic signal
        '''

    def __init__(self, config):
        self.config = config
        self.lane_phase_info = config['lane_phase_info']  # "intersection_1_1"

        self.intersection_id = list(self.lane_phase_info.keys())[0]
        self.phase_list = self.lane_phase_info[self.intersection_id]["phase"]
        self.phase_startLane_mapping = self.lane_phase_info[self.intersection_id]["phase_startLane_mapping"]

        self.phi = 20
        self.min_green_vehicle = 20
        self.max_red_vehicle = 30

        self.action = self.phase_list[0]

    def choose_action(self, state):
        cur_phase = state["current_phase"]
        if state["current_phase_time"] >= self.phi:
            num_green_vehicle = sum([state["lane_waiting_vehicle_count"][i] for i in self.phase_startLane_mapping[cur_phase]])
            num_red_vehicle = sum([state["lane_waiting_vehicle_count"][i] for i in self.lane_phase_info[self.intersection_id]["start_lane"]]) - num_green_vehicle
            if num_green_vehicle <= self.min_green_vehicle and num_red_vehicle > self.max_red_vehicle:
                self.action = cur_phase % len(self.phase_list) + 1
        return self.action


class DQNAgent:
    def __init__(self, config):
        self.state_size = config['state_size']
        self.action_size = config['action_size']
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        intersection_id = list(config['lane_phase_info'].keys())[0]
        self.phase_list = config['lane_phase_info'][intersection_id]['phase']

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(40, input_dim=self.state_size, activation='relu'))
        model.add(Dense(40, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        action = self.phase_list.index(action)
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:
            target = (reward + self.gamma *
                      np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)