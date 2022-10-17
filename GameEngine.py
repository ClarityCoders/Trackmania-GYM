from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys
from utils import save_replay_script, actions
import numpy as np

class MainClient(Client):
    def __init__(self, control_agent=False, block=False) -> None:
        self.state = None
        self.finished = False
        self.race_time = 0
        self.total_reward = 0
        self.current_checkpoint = 0
        self.max_race_time = 30000
        self.control_agent = control_agent
        self.block = block
        self.kill = False
        self.info_ready = False
        self.action = 0
        self.previous_action = {
            "accelerate":False,
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
        if not self.control_agent:
            iface.clear_event_buffer()
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
        inputs = iface.get_event_buffer().to_commands_str()
        self.race_time = _time
        # if _time == -10:
        #     print("-10")
        if self.race_time == -10:
            self.state = iface.get_simulation_state()
        if _time <= 0 and not self.control_agent:
            iface.set_input_state(
                sim_clear_buffer=True
            )
        if self.finished or self.race_time >= self.max_race_time:
            self.finished = True

        if (_time % 200 == 0 and _time >= 0) or self.finished:
            self.block = True
            reward = 0
            #reward += self.current_checkpoint
            if self.current_checkpoint == 3:
                reward += 10 * (self.max_race_time - self.race_time)
            state = iface.get_simulation_state()
            #drove off cliff
            if state.position[1] < 10:
                #print("OUCH")
                reward -= 1
            final_state = state.position
            distance = np.linalg.norm(state.velocity)

            if distance < 2 and _time > 400:
                self.finished = True

            final_state += [distance]
            previous_action = [
                int(self.previous_action["accelerate"]),
                int(self.previous_action["left"]),
                int(self.previous_action["right"]),
                int(self.previous_action["brake"]),
            ]
            #final_state += previous_action
            reward += distance * .005
            reward += self.current_checkpoint * 1
            self.total_reward += reward
            self.reward = reward
            self.state_env = final_state
            
            # Data is ready to be picked up
            self.info_ready = True
            while self.block:
                pass

            action = actions[self.action]

            #final = self.compare_actions(self.previous_action, action)
            #iface.set_input_state(**final)

            self.previous_action = {
                'sim_clear_buffer':False,
                "accelerate":action["accelerate"],
                "left":action["left"],
                "right":action["right"],
                "brake":action["brake"],
            }
            if not self.control_agent:
                iface.set_input_state(**self.previous_action)
        if self.finished or self.race_time >= self.max_race_time:
            inputs = iface.get_event_buffer().to_commands_str()
            save_replay_script(inputs, str(int(self.total_reward)))
            self.reset(iface)
            if not self.kill:
                iface.rewind_to_state(self.state)
            self.finished = False

    def reset(self, iface):
        iface.clear_event_buffer()
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
        print(f'Simulation finished: {self.total_reward}')


def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(MainClient(random_agent=False), server_name)


if __name__ == '__main__':
    main()