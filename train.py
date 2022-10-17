from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import VecMonitor
import os
from Trackmania_Custom_env import TrackmaniaENV
from utils import SaveOnBestTrainingRewardCallback


# Create log dir
log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)


def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.
    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = TrackmaniaENV(f"{env_id}{rank}")
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    env_id = "TMInterface"
    num_cpu = 4  # Number of processes to use
    # Create the vectorized environment
    env = VecMonitor(SubprocVecEnv([make_env(env_id, i) for i in [0,1,2,3]]),"tmp/TestMonitor")

    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./board/", learning_rate=0.0003)
    model = PPO.load("best.zip", env=env)
    print("------------- Start Learning -------------")
    callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)
    model.learn(total_timesteps=5000000, callback=callback, tb_log_name="PPO-0003-200MS-CheckpointsDiff")
    model.save(env_id)
    print("------------- Done Learning -------------")
