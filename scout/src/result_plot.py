import matplotlib.pyplot as plt
import numpy as np
import os

fig, ax = plt.subplots()
ax.set_title("TRAINNING RESULT")
ax.set_xlabel("EPISODE")
ax.set_ylabel("REWARD")

path_school = '/home/xyw/BUAA/Graduation/src/scout/result/img/'
path_home = r'E:\BUAA\Graduation Project\Mid-term report\Mine\src\scout\result\img'

def multi_para():
    for TRAIN_TIME in range(50):
        result_path = path_home + '\\PPO_%i.npy' %(TRAIN_TIME)
        if os.path.exists(result_path):
            reward_data = np.load(result_path)
            ax.plot(reward_data[0], reward_data[1], label = 'PPO_%i' %(TRAIN_TIME))
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
    single_para()