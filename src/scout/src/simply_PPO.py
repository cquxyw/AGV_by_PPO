"""
A simple version of Proximal Policy Optimization (PPO) using single thread.

Based on:
1. Emergence of Locomotion Behaviours in Rich Environments (Google Deepmind): [https://arxiv.org/abs/1707.02286]
2. Proximal Policy Optimization Algorithms (OpenAI): [https://arxiv.org/abs/1707.06347]

View more on my tutorial website: https://morvanzhou.github.io/tutorials

Dependencies:
tensorflow r1.2
gym 0.9.2
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import gym

EP_MAX = 1000
EP_LEN = 200
GAMMA = 0.9
A_LR = 0.0001
C_LR = 0.0002
BATCH = 32
A_UPDATE_STEPS = 10
C_UPDATE_STEPS = 10
S_DIM, A_DIM = 3, 1
#字典函数：dict(a='a',b='b'); 字典列表：method=[dict(),dict()]
METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]        # choose the method for optimization


class PPO(object):

    def __init__(self):
        # 会话控制：Session() -> sess.run()
        self.sess = tf.Session()
        # Session运行时输入值
        # tfs:状态输入
        self.tfs = tf.placeholder(tf.float32, [None, S_DIM], 'state')

        # critic
        with tf.variable_scope('critic'):
            # dense: densely-connected层，输入为tfs，使用relu激活函数，输出维度100，默认为增加变量到GraphKeys.TRAINABLE_VARIABLES，相当于tf.Variables,默认为使用bias参数，即w和b都在此定义
            l1 = tf.layers.dense(self.tfs, 100, tf.nn.relu)
            # 不输入激活函数时为linear action
            # v:参数w预测的value,v(s,w)
            self.v = tf.layers.dense(l1, 1)
            # tfdc_r: G，expected return,期望值
            self.tfdc_r = tf.placeholder(tf.float32, [None, 1], 'discounted_r')
            self.advantage = self.tfdc_r - self.v
            # squre()：对advantage里每个元素求平方
            # reduce_mean(input)：对input的tensor里所有元素求平均，返回一个值
            self.closs = tf.reduce_mean(tf.square(self.advantage))
            # AdamOptimizer: 训练优化器，学习率为C_LR，需要收敛closs的值
            self.ctrain_op = tf.train.AdamOptimizer(C_LR).minimize(self.closs)

        # actor
        pi, pi_params = self._build_anet('pi', trainable=True)
        oldpi, oldpi_params = self._build_anet('oldpi', trainable=False)
        with tf.variable_scope('sample_action'):
            # squeeze:删掉维度为1的多余的维度
            # sample:在多维正态分布里随机采样，采样数为1
            self.sample_op = tf.squeeze(pi.sample(1), axis=0)       # choosing action
        with tf.variable_scope('update_oldpi'):
            # [function(i) for i in list]: 循环执行function
            # zip(a,b):将列表a和列表b中对应元素分别组成元组，将这些元组再构成列表
            # for a,b in zip(ai,bi)，构成zip元组后，ai中对应值给a，bi对应值给b
            # assign(): oldp的值赋给p，创建节点名为update_oldpi_op
            self.update_oldpi_op = [oldp.assign(p) for p, oldp in zip(pi_params, oldpi_params)]

        self.tfa = tf.placeholder(tf.float32, [None, A_DIM], 'action')
        self.tfadv = tf.placeholder(tf.float32, [None, 1], 'advantage')
        with tf.variable_scope('loss'):
            with tf.variable_scope('surrogate'):
                # ratio = tf.exp(pi.log_prob(self.tfa) - oldpi.log_prob(self.tfa))
                
                # prob: method of class Normal, 计算tfa动作的概率
                ratio = pi.prob(self.tfa) / oldpi.prob(self.tfa)
                surr = ratio * self.tfadv
            if METHOD['name'] == 'kl_pen':
                self.tflam = tf.placeholder(tf.float32, None, 'lambda')
                # kl_divergence: 计算oldpi和pi两个概率的信息熵差值，*信息熵可作为最大期望算法的损失函数
                kl = tf.distributions.kl_divergence(oldpi, pi)
                self.kl_mean = tf.reduce_mean(kl)
                self.aloss = -(tf.reduce_mean(surr - self.tflam * kl))
            else:   # clipping method, find this is better
                # minimum: 返回surr和clip_by_value更小的那个
                self.aloss = -tf.reduce_mean(tf.minimum(
                    surr,
                    # clip_by_value: ratio为input,1-M为限制ratio的最小值，1+M为限制ratio最大值，超过限制将被赋值
                    tf.clip_by_value(ratio, 1.-METHOD['epsilon'], 1.+METHOD['epsilon'])*self.tfadv))

        with tf.variable_scope('atrain'):
            self.atrain_op = tf.train.AdamOptimizer(A_LR).minimize(self.aloss)

        # graph: a inherited method of Session, associated Graph
        # FileWriter: a Class of module summary, 将graph保存到log文件夹下
        tf.summary.FileWriter("log/", self.sess.graph)

        # global_variables_initializer: a method of tf, 初始化图中所有全局变量 (tf机制是在variable定义的时候仅仅是定义，只有在执行语句之后才真正给全局变量赋值)
        self.sess.run(tf.global_variables_initializer())

    def update(self, s, a, r):
        self.sess.run(self.update_oldpi_op)
        #run: 执行advantage函数，并将s赋值给tfs, r赋值给tfdc_r作为advantage输入值 (需要使用字典方式定义)
        adv = self.sess.run(self.advantage, {self.tfs: s, self.tfdc_r: r})
        # adv = (adv - adv.mean())/(adv.std()+1e-6)     # sometimes helpful

        # update actor
        if METHOD['name'] == 'kl_pen':
            for _ in range(A_UPDATE_STEPS):
                # a,b = session.run([ai,bi],{}):ai, bi都会执行，但不会执行公共部分，返回结果分别赋值给a,b
                _, kl = self.sess.run(
                    [self.atrain_op, self.kl_mean],
                    {self.tfs: s, self.tfa: a, self.tfadv: adv, self.tflam: METHOD['lam']})
                if kl > 4*METHOD['kl_target']:  # this in in google's paper
                    break
            if kl < METHOD['kl_target'] / 1.5:  # adaptive lambda, this is in OpenAI's paper
                METHOD['lam'] /= 2
            elif kl > METHOD['kl_target'] * 1.5:
                METHOD['lam'] *= 2
            # clip: numpy函数，限制lam对应数组的最大最小值
            METHOD['lam'] = np.clip(METHOD['lam'], 1e-4, 10)    # sometimes explode, this clipping is my solution
        else:   # clipping method, find this is better (OpenAI's paper)
            [self.sess.run(self.atrain_op, {self.tfs: s, self.tfa: a, self.tfadv: adv}) for _ in range(A_UPDATE_STEPS)]

        # update critic
        [self.sess.run(self.ctrain_op, {self.tfs: s, self.tfdc_r: r}) for _ in range(C_UPDATE_STEPS)]

    def _build_anet(self, name, trainable):
        with tf.variable_scope(name):
            l1 = tf.layers.dense(self.tfs, 100, tf.nn.relu, trainable=trainable)
            mu = 2 * tf.layers.dense(l1, A_DIM, tf.nn.tanh, trainable=trainable)
            sigma = tf.layers.dense(l1, A_DIM, tf.nn.softplus, trainable=trainable)
            # 求期望是mu,方差是sigma的正态分布
            norm_dist = tf.distributions.Normal(loc=mu, scale=sigma)
        # GLOBAL_VARIABLES是所有利用tf定义的变量
        # GraphKeys获取该变量
        # get_collection将这些变量列成列表形式    
        params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=name)
        return norm_dist, params

    def choose_action(self, s):
        # [newaxis,:]: 在newaxis语句的位置上增加一个维度
        s = s[np.newaxis, :]    
        a = self.sess.run(self.sample_op, {self.tfs: s})[0]
        return np.clip(a, -2, 2)

    def get_v(self, s):
        #ndim:numpy函数，输出s的维度
        if s.ndim < 2: s = s[np.newaxis, :]
        return self.sess.run(self.v, {self.tfs: s})[0, 0]

env = gym.make('Pendulum-v0').unwrapped
ppo = PPO()
all_ep_r = []

for ep in range(EP_MAX):
    # reset: 重置环境中的状态，如[角速度，角加速度，角度]等等
    s = env.reset()
    buffer_s, buffer_a, buffer_r = [], [], []
    ep_r = 0
    for t in range(EP_LEN):    # in one episode
        env.render()
        a = ppo.choose_action(s)
        # step:选择动作a，返回值: s_：目标的状态，r：动作或当前状态的reward，done：是否reset环境，_：可用于debug的信息
        s_, r, done, _ = env.step(a)
        # append: 将s加到列表buffer_s的末尾
        buffer_s.append(s)
        buffer_a.append(a)
        buffer_r.append((r+8)/8)    # normalize reward, find to be useful
        s = s_
        ep_r += r

        # update ppo
        if (t+1) % BATCH == 0 or t == EP_LEN-1:
            v_s_ = ppo.get_v(s_)
            discounted_r = []
            # b=a[i:j:s]:i-起始索引，缺省为0;j:结束索引，缺省为len(a);s:步长，缺省为1,为-1时表示从后到前
            for r in buffer_r[::-1]:
                v_s_ = r + GAMMA * v_s_
                discounted_r.append(v_s_)
            # reverse: 列表从后到前反向输出为新的列表
            discounted_r.reverse()

            # vstack((a,b)): 将数组a,b沿垂直放向叠加，在这里仅将列表转换成numpy array
            # array():创建数组
            bs, ba, br = np.vstack(buffer_s), np.vstack(buffer_a), np.array(discounted_r)[:, np.newaxis]
            buffer_s, buffer_a, buffer_r = [], [], []
            ppo.update(bs, ba, br)
    if ep == 0: all_ep_r.append(ep_r)
    else: all_ep_r.append(all_ep_r[-1]*0.9 + ep_r*0.1)
    print(
        'Ep: %i' % ep,
        "|Ep_r: %i" % ep_r,
        # function(a) if a>b else function(b): a>b成立时执行a，不成立时执行b
        # print("a=%d, b=%d" %(a,b))
        ("|Lam: %.4f" % METHOD['lam']) if METHOD['name'] == 'kl_pen' else '',
    )
# arange(a): 等差数组，a-数组包含多少个数，步长默认为1
# plot(x,y): 绘图，x-x轴上的数，y-y轴上的数
plt.plot(np.arange(len(all_ep_r)), all_ep_r)
plt.xlabel('Episode');plt.ylabel('Moving averaged episode reward');plt.show()