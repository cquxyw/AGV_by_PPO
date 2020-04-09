import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import interpolate

fig, ax = plt.subplots()
ax.set_title("TRAINNING RESULT")
ax.set_xlabel("EPISODE")
ax.set_ylabel("REWARD")

path_school = '/home/xyw/BUAA/Graduation/src/scout/result/img/'
path_home = r'E:\BUAA\Graduation Project\Mid-term report\Mine\src\scout\result\img'
color_list = ['blue', 'yellow', 'green', 'red', 'lime', 'orange', 'royalblue']

mean_size = 200

def multi_para():
    for TRAIN_TIME in range(50):
        result_path = path_home + '\\PPO_%i.npy' %(TRAIN_TIME)
        if os.path.exists(result_path):
            reward_data = np.load(result_path)
            # omit data which the episode is within 600
            if reward_data[1].size > 600:
                # delete the remainder number
                resize = reward_data[1].size - (reward_data[1].size % mean_size)
                s_reward = slice(0, resize)
                s_range = slice(0, resize, mean_size)
                s_reward_data = reward_data[1][s_reward]
                s_reward_range = reward_data[0][s_range]

                mean_reward_data = []
                max_reward_data = []
                min_reward_data = []

                for i in range(s_reward_range.size):
                    # choose slice range
                    s_temp = slice(i * mean_size, (i+1) * mean_size)

                    # count mean reward
                    mean_reward = np.mean(s_reward_data[s_temp])
                    mean_reward_data.append(mean_reward)

                    # count max reward
                    max_reward = np.max(s_reward_data[s_temp])
                    max_reward_data.append(max_reward)

                    # count min reward
                    min_reward = np.min(s_reward_data[s_temp])
                    min_reward_data.append(min_reward)

                # revert list to numpy
                mean_reward_data = np.array(mean_reward_data)
                max_reward_data = np.array(max_reward_data)
                min_reward_data = np.array(min_reward_data)

                # plot mean reward
                ax.plot(s_reward_range, mean_reward_data, label = 'PPO_%i' %(TRAIN_TIME), color = color_list[TRAIN_TIME])

                # plot max and min reward
                ax.plot(s_reward_range, max_reward_data, color = color_list[TRAIN_TIME], alpha=0.2)
                ax.plot(s_reward_range, min_reward_data, color = color_list[TRAIN_TIME], alpha=0.2)
                ax.fill_between(s_reward_range, max_reward_data, min_reward_data, color = color_list[TRAIN_TIME], alpha=0.2)

                # show the label
                ax.legend()
        plt.savefig(path_home + '\\result_multi.png')

def single_para():
    reward_data_all = np.array([])
    reward_range = 0
    for TRAIN_TIME in range(50):
        result_path = path_home + '\\PPO_%i.npy' %(TRAIN_TIME)
        if os.path.exists(result_path):
            reward_data = np.load(result_path)
            reward_data_all = np.concatenate([reward_data_all, reward_data[1]])
            reward_range += reward_data[0].size
    reward_range_array = np.arange(reward_range)
    ax.plot(reward_range_array, reward_data_all, label = 'PPO')
    ax.legend()
    plt.savefig(path_home + '\\result_single.png')

if __name__ == '__main__':
    multi_para()