from Trackmania_Custom_env import TrackmaniaENV
import random
import time
import pickle

start_time = time.time()
actions = [1] * 1000
random.seed(1989)
locations = []

def main():
    distance_checkpoint = 0
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
        distance_checkpoint += obs[3]
        if steps == 1:
            start_time = time.time()
        #elif steps % 5 == 0 and steps > 0:
        elif distance_checkpoint >= 150 and steps > 0:
            locations.append([obs[0],obs[1],obs[2], steps, distance_checkpoint])
            distance_checkpoint = 0
            #print("CHECK")
        action = env.action_space.sample()
        obs, rew, done, info = env.step(random.randint(1,3))
        print(obs, steps)
        #env.render()
        reward_total += rew
        if done:
            #print(obs)
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
    print(len(locations))
    print(locations)

    # Used to create checkpoints
    # filename = 'checkpoints61'
    # file = open(filename, 'wb')
    # pickle.dump(locations, file)
    # file.close()

if __name__ == "__main__":
    main()