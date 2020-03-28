import matplotlib.pyplot as plt
import numpy as np
import os

fig, ax = plt.subplots()
ax.set_title("TRAINNING RESULT")
ax.set_xlabel("EPISODE")
ax.set_ylabel("REWARD")

def filter(reward_data):
    reward_plot = np.array([])
    mean_data = np.array([])
    for i in range(reward_data[0].size):
        mean_data = np.append(mean_data, reward_data[1][i])
        if (i+1) % 20 == 0:
            mean_reward = np.mean(mean_data)
            reward_plot = np.append(reward_plot, mean_reward)
            mean_data = np.array([])
        elif i == 0:
            reward_plot = np.append(reward_plot, mean_reward)
    return reward_plot

if __name__ == '__main__':
    
    for TRAIN_TIME in range(50):
        result_path = '/home/xyw/BUAA/Graduation/src/scout/result/img/PPO_%i.npy' %(i)
        if os.path.exists(result_path):
            reward_data = np.load(result_path)
            reward_plot = filter(reward_data)
            ax.plot(reward_data[0], reward_plot, label = 'PPO_%i' %(TRAIN_TIME))
            ax.legend()
    plt.savefig('/home/xyw/BUAA/Graduation/src/scout/result/img/result.eps')