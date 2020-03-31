import matplotlib.pyplot as plt
import numpy as np
import os

fig, ax = plt.subplots()
ax.set_title("TRAINNING RESULT")
ax.set_xlabel("EPISODE")
ax.set_ylabel("REWARD")

path_school = '/home/xyw/BUAA/Graduation/src/scout/result/img/'
path_home = r'E:\BUAA\Graduation Project\Mid-term report\Mine\src\scout\result\img'

def filter(reward_data):
    reward_plot = np.array([])
    mean_data = np.array([])
    for i in range(reward_data[1].size):
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
        result_path = path_school + 'PPO_%i.npy' %(TRAIN_TIME)
        if os.path.exists(result_path):
            reward_data = np.load(result_path)
            reward_plot = filter(reward_data)
            ax.plot(reward_data[0], reward_plot, label = 'PPO_%i' %(TRAIN_TIME))
            ax.legend()
    plt.savefig(path_school + 'result.eps')