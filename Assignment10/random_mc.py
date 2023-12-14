import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
import random


def random_mc(env, max_steps):

    steps = 0
    env.reset()
    done = False
    while not done and steps < max_steps:

        action = random.randint(0, 2)
        new_state, reward, done, truncated, info = env.step(action)

        steps = steps + 1
        print("Steps {}   Reward {} ".format(steps, reward))

    print("Num Steps To Complete {}".format(steps))

    return steps



# Import and initialize Mountain Car Environment
env = gym.make('MountainCar-v0')
env.reset()

max_steps = 10000000
num_to_avg = 3

num_steps = []
for i in range(num_to_avg):
    print("Episode {}".format(i))
    num_steps.append(random_mc(env, max_steps))

avg_num_steps = sum(num_steps)/len(num_steps)

print("Avg number of steps required {}".format(avg_num_steps))