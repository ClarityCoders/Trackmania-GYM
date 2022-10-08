from random import seed
import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
import numpy as np
from RandomSim import MainClient
from tminterface.interface import TMInterface
import time
import signal

class TrackmaniaENV(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, server_name="TMInterface0"):
        super(TrackmaniaENV, self).__init__()

        print(f'Connecting to {server_name}...')
        self.client = MainClient(random_agent=False, block=True)

        # Start Server
        self.iface = TMInterface(server_name)

        def handler(signum, frame):
            self.iface.close()
            quit()

        signal.signal(signal.SIGBREAK, handler)
        signal.signal(signal.SIGINT, handler)
        self.iface.register(self.client)

        while not self.iface.registered:
            time.sleep(0)
        print("HEY")

        low = np.array(
            [
                #Positional Elements
                # X,Y,X
                0,
                0,
                0,
                # Distance
                0,
                # Previous Inputs
                0,
                0,
                0,
                0
            ]
        ).astype(np.float32)
        high = np.array(
            [
                #Positional Elements
                # X,Y,Z
                2000,
                2000,
                2000,
                # Distance
                2000,
                # Previous Inputs
                1,
                1,
                1,
                1
            ]
        ).astype(np.float32)

        self.observation_space = spaces.Box(low, high,seed=1989)
        self.action_space = spaces.Discrete(7)

    def step(self, action):
        observation = [0,0,0,0,0,0,0,0]
        reward = 0
        done = False
        info = {}
        #time.sleep(2.01)
        #print(client.info_ready)
        while not self.client.info_ready:
            time.sleep(0)
        if self.client.info_ready:
            self.client.action = action
            state = self.client.state_env
            reward = self.client.reward
            game_time = self.client.race_time
            self.client.info_ready = False
            self.client.block = False
            done = self.client.finished
            #print(state, reward, game_time)
        observation = np.array(state, dtype=np.float32)
        return observation, reward, done, info
    def reset(self):
        observation = np.array([0,0,0,0,0,0,0,0], dtype=np.float32)
        print("reset")
        return observation  # reward, done, info can't be included
    def render(self, mode='human'):
        pass
    def close (self):
        self.client.kill = True
        self.client.block = False
        #print("Sleep Before Kill")
        self.iface.close()
        time.sleep(10)
        #print("after Kill")
        self.client = None
        self.iface = None

if __name__ == "__main__":
    env = TrackmaniaENV()
    # It will check your custom environment and output additional warnings if needed
    check_env(env)