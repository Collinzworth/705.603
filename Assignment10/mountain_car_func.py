import numpy as np

def print_avg_reward(episode_num, avg_rewards, reward_list, print_interval):

    # Average reward for last n episodes
    if (episode_num + 1) % print_interval == 0:
        avg_reward = np.mean(reward_list)
        avg_rewards.append(avg_reward)
        reward_list = []

    if (episode_num + 1) % print_interval == 0:    
        print('Episode {} Average Reward: {}'.format(episode_num + 1, avg_reward))

    print("Episode {}".format(episode_num))

    return avg_rewards, reward_list

def discretize_state(env, state):
    # Discretize state
    state_adj = (state - env.observation_space.low)*np.array([10, 100])
    state_adj = np.round(state_adj, 0).astype(int)
    return state_adj

def select_action(Q, env, state_adj, epsilon):
    # Determine next action - epsilon greedy strategy
    if np.random.random() < 1 - epsilon:
        action = np.argmax(Q[state_adj[0], state_adj[1]]) 
    else:
        action = np.random.randint(0, env.action_space.n)

    return action

def video_capture(env, video, num_episodes, episode_num):
    # Render environment for last five episodes
    if episode_num >= (num_episodes - 20):
        env.render()
        video.capture_frame()

