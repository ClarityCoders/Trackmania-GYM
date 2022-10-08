from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys
from utils import save_replay_script, actions
import random
import numpy as np

class MainClient(Client):
    def __init__(self, random_agent=False, block=False) -> None:
        self.state = None
        self.finished = False
        self.race_time = 0
        self.total_reward = 0
        self.current_checkpoint = 0
        self.max_race_time = 30000
        self.random_agent = random_agent
        self.block = block
        self.kill = False
        self.info_ready = False
        self.action = 0
        self.previous_action = {
            "accelerate":True,
            "left":False,
            "right":False,
            "brake":False,
        }
        super(MainClient, self).__init__()

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')
        iface.set_timeout(200000)

    def on_simulation_begin(self, iface: TMInterface):
        iface.remove_state_validation()
        self.finished = False

    def compare_actions(self, previous, current):
        final = {'sim_clear_buffer':False}
        if previous['accelerate'] != current['accelerate']:
            final['accelerate'] = current['accelerate']
        if previous['left'] != current['left']:
            final['left'] = current['left']
        if previous['right'] != current['right']:
            final['right'] = current['right']
        if previous['brake'] != current['brake']:
            final['brake'] = current['brake']
        return final

    def on_simulation_step(self, iface: TMInterface, _time: int):
        if self.race_time == 0:
            self.state = iface.get_simulation_state()
        if _time < 0:
            iface.set_input_state(
                sim_clear_buffer=True
            )
        if self.finished or self.race_time >= self.max_race_time:
            self.finished = True

        self.block = True
        reward = 0
        reward += self.current_checkpoint
        if self.current_checkpoint == 3:
            reward += (self.max_race_time - self.race_time)
        self.race_time = _time
        state = iface.get_simulation_state()
        final_state = state.position
        distance = np.linalg.norm(state.velocity)
        final_state += [distance]
        previous_action = [
            int(self.previous_action["accelerate"]),
            int(self.previous_action["left"]),
            int(self.previous_action["right"]),
            int(self.previous_action["brake"]),
        ]
        final_state += previous_action
        reward += distance * .00001
        reward += self.current_checkpoint * .01
        self.total_reward += reward
        self.reward = reward
        self.state_env = final_state
        
        # Data is ready to be picked up
        self.info_ready = True
        while self.block:
            pass

        action = actions[self.action]
        if _time % 200 == 0:
            final = self.compare_actions(self.previous_action, action)
            iface.set_input_state(**final)

            self.previous_action = {
                "accelerate":action["accelerate"],
                "left":action["left"],
                "right":action["right"],
                "brake":action["brake"],
            }

        if self.finished or self.race_time >= self.max_race_time:
            inputs = iface.get_event_buffer().to_commands_str()
            save_replay_script(inputs, str(int(self.total_reward)))
            self.reset()
            if not self.kill:
                iface.rewind_to_state(self.state)
            self.finished = False

    def reset(self):
        self.total_reward = 0
        self.current_checkpoint = 0

    def on_checkpoint_count_changed(self, iface: TMInterface, current: int, target: int):
        self.current_checkpoint = current
        if current == target:
            print(f'Finished the race at {self.race_time}')
            self.finished = True
            if not self.kill:
                iface.prevent_simulation_finish()

    def on_simulation_end(self, iface, result: int):
        print('Simulation finished')


def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(MainClient(random_agent=False), server_name)


if __name__ == '__main__':
    main()