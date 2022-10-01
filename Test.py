from tminterface.interface import TMInterface
from tminterface.structs import BFEvaluationDecision, BFEvaluationInfo, BFEvaluationResponse, BFPhase
from tminterface.client import Client, run_client
import sys
import keyboard
import pickle

class MainClient(Client):
    def __init__(self) -> None:
        self.current_time = 0
        self.phase = BFPhase.INITIAL
        super(MainClient, self).__init__()
        self.key_presses = []

    def on_registered(self, iface: TMInterface) -> None:
        iface.set_timeout(-1)
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time >= 0:
            state = iface.get_simulation_state()
            input_string = []
            if keyboard.is_pressed("left"):
                input_string.append("0")
            if keyboard.is_pressed("up"):
                input_string.append("1")
            if keyboard.is_pressed("right"):
                input_string.append("2")
            if keyboard.is_pressed("down"):
                input_string.append("3")
                
            self.key_presses.append("".join(input_string))
                

            #print(
            #     f'Time: {_time}\n' 
            #     f'Display Speed: {state.display_speed}\n'
            #     f'Position: {state.position}\n'
            #     f'Velocity: {state.velocity}\n'
            #     f'YPW: {state.yaw_pitch_roll}\n'
            # )

    def on_checkpoint_count_changed(self, iface: TMInterface, current: int, target: int):
        print(current, target)
        if target == current:
            print(self.key_presses)
            dbfile = open('exampleRun', 'ab')
      
            # source, destination
            pickle.dump(self.key_presses, dbfile)                     
            dbfile.close()


def main():
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(type(server_name))
    print(f'Connecting to {server_name}...')
    run_client(MainClient(), server_name)


if __name__ == '__main__':
    main()