from http import server
from tminterface.interface import TMInterface
from tminterface.structs import BFEvaluationDecision, BFEvaluationInfo, BFEvaluationResponse, BFPhase
from tminterface.client import Client, run_client
import sys
import keyboard
import pickle
import time
from utils.directkeys import PressKey, ReleaseKey, W, A, S, D

class MainClient(Client):
    def __init__(self) -> None:
        self.current_time = 0
        self.phase = BFPhase.INITIAL
        super(MainClient, self).__init__()
        dbfile = open('TestRun3094', 'rb')     
        db = pickle.load(dbfile)
        self.key_presses = db
        print(self.key_presses)
        print(len(self.key_presses))

    def on_registered(self, iface: TMInterface) -> None:
        iface.set_timeout(20000)
        print(iface.get_context_mode())
        print(f'Registered to {iface.server_name}')

    def on_run_step(self, iface: TMInterface, _time: int):
        if _time >= 0 and len(self.key_presses) > 0:
            state = iface.get_simulation_state()
            current_keys = self.key_presses[0]
            ReleaseKey(A)
            ReleaseKey(W)
            ReleaseKey(D)
            ReleaseKey(S)
            #test = input()
            for key in current_keys:
                if key == "0":
                    PressKey(A)
                elif key == "1":
                    PressKey(W)
                elif key == "2":
                    PressKey(D)
                elif key == "3":
                    PressKey(S)
            self.key_presses.pop(0)

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
    print(f'Connecting to {server_name}...')
    run_client(MainClient(), server_name)


if __name__ == '__main__':
    main()