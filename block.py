from tracemalloc import start
from tminterface.client import Client, run_client
from RandomSim import MainClient
import sys
import time
import threading
from multiprocessing import Process

server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
print(f'Connecting to {server_name}...')
Game_Engine = MainClient(random_agent=True, block=True)

#x = threading.Thread(target=run_client, args=(Game_Engine, server_name))
def gym_example():
    while True:
        time.sleep(2.01)
        #print(Game_Engine.info_ready)
        if Game_Engine.info_ready:
            state = Game_Engine.state
            reward = Game_Engine.reward
            game_time = Game_Engine.race_time
            Game_Engine.info_ready = False
            Game_Engine.block = False
            print(state, reward, game_time)

def start_engine():
    run_client(Game_Engine, server_name)

x = Process(target=gym_example)
x.start()
run_client(Game_Engine, server_name)
#y = threading.Thread(target=start_engine)
#y.start()
# p = Process(target=start_engine)
# p.start()