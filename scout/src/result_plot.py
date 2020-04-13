import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import interpolate

path_school = '/home/xyw/BUAA/Graduation/src/scout/result/img/'
path_home = r'E:\BUAA\Graduation Project\Mid-term report\Mine\src\scout\result\img'
color_list = ['blue', 'yellow', 'green', 'red', 'lime', 'orange', 'royalblue']

mean_size = 100
data_num = 20

def multi_para():

    fig1, ax1 = plt.subplots()
    ax1.set_title("TRAINNING RESULT")
    ax1.set_xlabel("EPISODE")
    ax1.set_ylabel("REWARD")

    for TRAIN_TIME in range(data_num):
        result_path = path_home + '\\PPO_%i.npy' %(TRAIN_TIME)
        if os.path.exists(result_path):
            reward_data = np.load(result_path)
            # omit data which the episode is within mean_size
            if reward_data[1].size > mean_size:
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
                ax1.plot(s_reward_range, mean_reward_data, label = 'PPO_%i' %(TRAIN_TIME), color = color_list[TRAIN_TIME])

                # plot max and min reward
                ax1.plot(s_reward_range, max_reward_data, color = color_list[TRAIN_TIME], alpha=0)
                ax1.plot(s_reward_range, min_reward_data, color = color_list[TRAIN_TIME], alpha=0)
                ax1.fill_between(s_reward_range, max_reward_data, min_reward_data, color = color_list[TRAIN_TIME], alpha=0.2)

                # show the label
                ax1.legend()
        plt.savefig(path_home + '\\result_multi.png')

def single_para():

    fig2, ax2 = plt.subplots()
    ax2.set_title("TRAINNING RESULT")
    ax2.set_xlabel("EPISODE")
    ax2.set_ylabel("REWARD")

    reward_data_all = np.array([])
    reward_range = 0

    for TRAIN_TIME in range(data_num):
        result_path = path_home + '\\PPO_%i.npy' %(TRAIN_TIME)
        if os.path.exists(result_path):
            # load data
            reward_data = np.load(result_path)

            # add seperate data to one array
            reward_data_all = np.concatenate([reward_data_all, reward_data[1]])
            reward_range += reward_data[0].size
            reward_range_array = np.arange(reward_range)

            # slice data
            resize = reward_data_all.size - (reward_data_all.size % mean_size)
            s_reward = slice(0, resize)
            s_range = slice(0, resize, mean_size)
            s_reward_data = reward_data_all[s_reward]
            s_reward_range = reward_range_array[s_range]

            mean_reward_data = []
            max_reward_data = []
            min_reward_data = []

            # culculate mean, max and min data in slice range
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

            # revert data list to numpy
            mean_reward_data = np.array(mean_reward_data)
            max_reward_data = np.array(max_reward_data)
            min_reward_data = np.array(min_reward_data)

    # plot mean reward
    Color = color_list[6]

    ax2.plot(s_reward_range, mean_reward_data, label = 'PPO', color = Color)

    # plot max and min reward
    ax2.plot(s_reward_range, max_reward_data, color = Color, alpha=0)
    ax2.plot(s_reward_range, min_reward_data, color = Color, alpha=0)
    ax2.fill_between(s_reward_range, max_reward_data, min_reward_data, color = Color, alpha=0.2)

    # ax.plot(reward_range_array, reward_data_all, label = 'PPO')
    ax2.legend()
    plt.savefig(path_home + '\\result_single.png')

if __name__ == '__main__':
    single_para()
    multi_para()