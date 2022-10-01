from tminterface.interface import TMInterface
from tminterface.client import Client, run_client
import sys
import time
from utils import save_replay_script, actions
import random

class MainClient(Client):
    def __init__(self) -> None:
        self.state = None
        self.finished = False
        self.race_time = 0
        self.current_checkpoint = 0
        self.max_race_time = 30000
        super(MainClient, self).__init__()

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')
        iface.set_timeout(200000)

    def on_simulation_begin(self, iface: TMInterface):
        iface.remove_state_validation()
        self.finished = False

    def on_simulation_step(self, iface: TMInterface, _time: int):
        self.race_time = _time
        state = iface.get_simulation_state()
        
        #iface.set_input_state(sim_clear_buffer=False, left=True)
        if self.race_time == 0:
            self.state = iface.get_simulation_state()

        action = random.choice(actions)
        #print(iface.get_event_buffer().to_commands_str())
        if _time % 100 == 0:
            iface.set_input_state(
                sim_clear_buffer=False, 
                accelerate=action["accelerate"], 
                left=action["left"], 
                right=action["right"],
                brake=action["brake"]
            )
        #else:
        #    iface.set_input_state(sim_clear_buffer=False, accelerate=False)

        if self.finished or self.race_time >= self.max_race_time:
            print(self.current_checkpoint)
            save_replay_script(iface, str(self.current_checkpoint))
            iface.rewind_to_state(self.state)
            self.finished = False

    def on_checkpoint_count_changed(self, iface: TMInterface, current: int, target: int):
        self.current_checkpoint = current
        if current == target:
            print(f'Finished the race at {self.race_time}')
            self.finished = True
            iface.prevent_simulation_finish()

    def on_simulation_end(self, iface, result: int):
        print('Simulation finished')


def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    run_client(MainClient(), server_name)


if __name__ == '__main__':
    main()