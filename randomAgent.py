from Trackmania_Custom_env import TrackmaniaENV
import random
import time
start_time = time.time()

random.seed(1989)
def main():
    steps = 0
    #env = retro.make(game='MegaMan2-Nes')
    env = TrackmaniaENV("TMInterface0")
    env.seed(1989)
    obs = env.reset()
    print(obs.shape)
    done = False
    reward_total = 0
    env.action_space.np_random.seed(123)
    while not done:
        if steps == 1:
            start_time = time.time()
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)
        #print(action)
        #env.render()
        reward_total += rew
        if done:
            obs = env.reset()
        steps += 1
        #print(rew)
        if steps % 1000 == 0:
            print(f"Total Steps: {steps}")

    print(f"--- {time.time() - start_time} seconds ---")
    print("Final Info")
    print(f"Total Steps: {steps}")
    print(reward_total)
    env.close()


if __name__ == "__main__":
    main()