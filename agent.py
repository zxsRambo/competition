import pandas as pd
import os

class FixedtimeAgent():

    def __init__(self, config):
        self.config = config

        self.current_phase_time = 1
        self.fixed_time = 30
        self.phase_list = config['phase_list']
        self.phase_id = 0
        self.phase_log = []
        self.yellow_fixed_time = 5
        self.yellow_start = 0
        self.yellow_flag = False



    def choose_action(self, state):
        if self.yellow_flag:
            if state['current_time'] - self.yellow_start >= self.yellow_fixed_time:
                self.phase_id = (self.phase_id + 1) % len(self.phase_list)
                self.yellow_flag = False
            self.phase_log.append(0)
            return 0  # 0 represents yellow signal
        else:
            if self.current_phase_time >= self.fixed_time:
                self.current_phase_time = 1
                self.yellow_start = state['current_time']
                self.yellow_flag = True
            else:
                self.current_phase_time += 1

            self.phase_log.append(self.phase_list[self.phase_id])

            return self.phase_list[self.phase_id]

    def log(self):
        df = pd.DataFrame({'phase': self.phase_log})
        df.to_csv(os.path.join(self.config['records_path'], 'signal_timing.txt'), index=None)

