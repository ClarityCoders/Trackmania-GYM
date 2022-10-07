from tracemalloc import start
from tminterface.client import Client, run_client
from RandomSim import MainClient
import sys
import time
import threading
from multiprocessing import Process
from tminterface.interface import TMInterface

import time
import signal

server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
print(f'Connecting to {server_name}...')
client = MainClient(random_agent=True, block=True)

#x = threading.Thread(target=run_client, args=(client, server_name))
def gym_example():
    while True:
        time.sleep(2.01)
        print("HEY")
        #print(client.info_ready)
        if client.info_ready:
            state = client.state
            reward = client.reward
            game_time = client.race_time
            client.info_ready = False
            client.block = False
            print(state, reward, game_time)

def start_engine():
    run_client(client, server_name)

#x = Process(target=gym_example)
#x.start()
#run_client(client, server_name)
#y = threading.Thread(target=start_engine)
#y.start()
# p = Process(target=start_engine)
# p.start()

#server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
#print(f'Connecting to {server_name}...')
#client = MainClient()
iface = TMInterface(server_name)

def handler(signum, frame):
    iface.close()
    quit()

signal.signal(signal.SIGBREAK, handler)
signal.signal(signal.SIGINT, handler)
iface.register(client)

while not iface.registered:
    time.sleep(0)
print("HEY")
gym_example()