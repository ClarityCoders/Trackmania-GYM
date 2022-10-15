from cmath import inf
from random import seed
import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
import numpy as np
from GameEngine import MainClient
from tminterface.interface import TMInterface
import time
import signal
import pickle

class TrackmaniaENV(gym.Env):
    """
    Custom Environment that follows gym interface
    Pulls in data from GameEngine.py
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, server_name="TMInterface0"):
        super(TrackmaniaENV, self).__init__()

        # Load Checkpoints
        filename = 'CheckpointsReady'
        unpickleFile = open(filename, 'rb')
        self.checkpoints = pickle.load(unpickleFile, encoding='bytes')
        unpickleFile.close()

        print(f'Connecting to {server_name}...')
        self.client = MainClient(control_agent=False, block=True)

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
                0
            ]
        ).astype(np.float32)
        high = np.array(
            [
                #Positional Elements
                # X,Y,Z
                200,
                200,
                200,
                # Distance
                500,
            ]
        ).astype(np.float32)

        self.observation_space = spaces.Box(low, high,seed=1989)
        self.action_space = spaces.Discrete(7)
        self.steps = 0
        self.checkpoints_local = [[0,0,0,0]]

    def step(self, action):
        observation = [0,0,0,0]
        self.steps += 1
        reward = 0
        done = False
        info = {}

        # If we have more than one checkpoint
        # See if we need to advance the checkpoint
        if len(self.checkpoints_local) > 1:
            if self.checkpoints_local[0][3] < self.steps:
                self.checkpoints_local.pop(0)

        # Block until the GameEngine.py data is ready.
        while not self.client.info_ready:
            time.sleep(0)
        
        # Data now ready
        if self.client.info_ready:
            
            # Send our action to the game Engine
            self.client.action = action

            # Get the state from GameEngine.py
            #state = self.client.state_env
            state = [
                self.client.state_env[0] - self.checkpoints_local[0][0],
                self.client.state_env[1] - self.checkpoints_local[0][1],
                self.client.state_env[2] - self.checkpoints_local[0][2],
                self.client.state_env[3]
            ]
            # Add our checkpoint
            #state += [self.checkpoints_local[0][0], self.checkpoints_local[0][1], self.checkpoints_local[0][2]]
            # Get Reward from GameEngine.py
            # This should probably be moved to the ENV
            reward = self.client.reward

            # Set it to block next turn
            self.client.info_ready = False
            self.client.block = False
            done = self.client.finished

        observation = np.array(state, dtype=np.float32)
        return observation, reward, done, info
    def reset(self):
        self.steps = 0
        self.checkpoints_local = self.checkpoints.copy()
        observation = np.array([0,0,0,0], dtype=np.float32)
        return observation  # reward, done, info can't be included
    def render(self, mode='human'):
        pass
    def close (self):
        self.client.kill = True
        self.client.block = False

        self.iface.close()
        time.sleep(10)

        self.client = None
        self.iface = None

if __name__ == "__main__":
    env = TrackmaniaENV()
    # It will check your custom environment and output additional warnings if needed
    check_env(env)