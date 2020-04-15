# artificial potential field approach
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import math

q = 1
n = 1

class field_mat(object):

    def __init__(self):
        self.goal = np.array([3,4])
        self.current_obs_info = np.array([[1,1], [0,0]])
        self.me = np.array([0.3, 0.3])

    def cal_mat(self):
        me_round = np.round(self.me)
        u_mat = np.empty([20, 20])
        for row in range(20):
            for line in range(20):
                row_i = row - 10
                line_i = line - 10
                ur = self.ur_val(row_i, line_i, me_round, self.current_obs_info)
                ua = self.ua_val(row_i, line_i, me_round, self.goal)
                u = ur + ua
                u_mat[row][line] = u
        return u_mat

    def ur_val(self, row_i, line_i, me, current_obs_info):
        ur = 0
        dis_array = []
        for i in range(np.shape(current_obs_info)[0]):
            x = (me[0] - row_i) - current_obs_info[i][0]
            y = (me[1] - line_i) - current_obs_info[i][1]
            dis = math.hypot(x, y)
            dis_array.append(dis)
        dis_array = np.array(dis_array)
        dis_min = np.min(dis_array)
        dis_min = np.clip(dis_min, 1e-5, 1e+5)
        if dis_min > q:
            ur = 0
        if dis_min < q:
            ur = 1/2 * n * pow((1/dis_min - 1/q), 2)
        return ur

    def ua_val(self, row_i, line_i, me, goal):
        ua = 0
        x = (me[0] - row_i) - goal[0]
        y = (me[1] - line_i) - goal[1]
        ua = math.hypot(x, y)
        return ua

if __name__ == '__main__':
    mat = field_mat()
    u = mat.cal_mat()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.zeros([20, 20])
    y = np.zeros([20, 20])
    for i in range(20):
        x[i] = np.arange(0, 20,1)
        y[i] = np.arange(0,20,1)
    z = u
    print(x, y)

    ax.plot_wireframe(x, y, z)
    plt.show()

    # print(u)