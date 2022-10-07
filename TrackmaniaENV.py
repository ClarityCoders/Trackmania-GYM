import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
import numpy as np
import threading
from RandomSim import MainClient

class Trackmania(gym.Env,threading.Thread):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(Trackmania, self).__init__()
        threading.Thread.__init__(self)
        server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
        print(f'Connecting to {server_name}...')
        self.Game_Engine = MainClient(random_agent=True, block=True)
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

        self.observation_space = spaces.Box(low, high)
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        observation = [0,0,0,0,0,0,0,0]
        reward = 0
        done = False
        info = {}

        return observation, reward, done, info
    def reset(self):
        observation = np.array([0,0,0,0,0,0,0,0], dtype=np.float32)
        return observation  # reward, done, info can't be included
    def render(self, mode='human'):
        pass
    def close (self):
        pass

if __name__ == "__main__":
    env = Trackmania()
    # It will check your custom environment and output additional warnings if needed
    check_env(env)