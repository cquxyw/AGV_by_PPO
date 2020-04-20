import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import logging

GAMMA = 0.9
A_UPDATE_STEPS = 30
C_UPDATE_STEPS = 30
S_TYPE = 3
S_TYPE_DIM = 4
A_DIM = 2
METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]        # choose the method for optimization

class ppo(object):

    def __init__(self, TRAIN_TIME):
        self.sess = tf.Session()
        self.tfs = tf.placeholder(tf.float32, [None, S_TYPE, S_TYPE_DIM], 'state')
        self.TRAIN_TIME = TRAIN_TIME
        
        # self.A_LR = 1e-7
        # self.C_LR = 2e-7
        
        # self.A_LR = np.random.rand() * self.C_LR
        # self.C_LR = pow(10, np.random.uniform(-4, -9))

        # self.A_LR = pow(10, np.random.uniform(-5, -6)) 
        # self.C_LR = 2 * self.A_LR

        self.A_LR = 8e-7 * pow(0.8, self.TRAIN_TIME)
        self.C_LR = 2 * self.A_LR

        self.alossr = 0
        self.clossr = 0

        self.logger = logging.getLogger('ppo_train')
        self.handler = logging.FileHandler('/home/xyw/BUAA/Graduation/src/scout/result/multi/log/PPO_Log.txt')
        self.fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'    
        self.formatter = logging.Formatter(self.fmt)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.NOTSET)

        # critic
        with tf.variable_scope('critic'):

            split_car = tf.layers.conv1d(self.tfs[:, 0:1, :], 64, 1, strides = 1, activation=tf.nn.tanh)
            split_obs = tf.layers.conv1d(self.tfs[:, 1:2, :], 64, 1, strides = 1, activation=tf.nn.tanh)
            split_goal = tf.layers.dense(self.tfs[:, 2:3, 0:2], 64, tf.nn.tanh)

            split_car_flat = tf.layers.flatten(split_car)
            split_obs_flat = tf.layers.flatten(split_obs)
            split_goal_flat = tf.layers.flatten(split_goal)

            merge_net = tf.keras.layers.concatenate([split_car_flat, split_obs_flat, split_goal_flat])

            input_net = tf.layers.dense(merge_net, 128, tf.nn.tanh)

            self.v = tf.layers.dense(input_net, 1)
            self.tfdc_r = tf.placeholder(tf.float32, [None, 1], 'discounted_r')
            self.advantage = self.tfdc_r - self.v
            self.closs = tf.reduce_mean(tf.square(self.advantage))
            self.ctrain_op = tf.train.AdamOptimizer(self.C_LR).minimize(self.closs)

        # actor
        pi, pi_params = self._build_anet('pi', trainable=True)
        oldpi, oldpi_params = self._build_anet('oldpi', trainable=False)

        with tf.variable_scope('sample_action'):
            self.sample_op = tf.squeeze(pi.sample(1), axis=0)       # choosing action
            self.get_mu = pi.mean()
            self.get_sigma = pi.variance()
        with tf.variable_scope('update_oldpi'):
            self.update_oldpi_op = [oldp.assign(p) for p, oldp in zip(pi_params, oldpi_params)]

        self.tfa = tf.placeholder(tf.float32, [None, A_DIM], 'action')
        self.tfadv = tf.placeholder(tf.float32, [None, 1], 'advantage')

        with tf.variable_scope('loss'):
            with tf.variable_scope('surrogate'):
                ratio = pi.prob(self.tfa) / tf.clip_by_value(oldpi.prob(self.tfa), 1e-5, 1e+5)
                # ratio = tf.exp(pi.prob(self.tfa) - oldpi.prob(self.tfa))
                surr = ratio * self.tfadv

            self.aloss = -tf.reduce_mean(tf.minimum(
                surr,
                tf.clip_by_value(ratio, 1.-METHOD['epsilon'], 1.+METHOD['epsilon'])*self.tfadv))

        with tf.variable_scope('atrain'):
            self.atrain_op = tf.train.AdamOptimizer(self.A_LR).minimize(self.aloss)

        # tf.summary.FileWriter("/home/xyw/BUAA/Graduation/src/scout/result/log/", self.sess.graph)
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()

    def update(self, s, a, r):
        self.sess.run(self.update_oldpi_op)
        adv = self.sess.run(self.advantage, {self.tfs: s, self.tfdc_r: r})
        
        # update actor
        [self.sess.run(self.atrain_op, {self.tfs: s, self.tfa: a, self.tfadv: adv}) for _ in range(A_UPDATE_STEPS)]
        self.alossr = self.sess.run(self.aloss, {self.tfs: s, self.tfa: a, self.tfadv: adv})

        # update critic
        [self.sess.run(self.ctrain_op, {self.tfs: s, self.tfdc_r: r}) for _ in range(C_UPDATE_STEPS)]
        self.clossr = self.sess.run(self.closs, {self.tfs: s, self.tfdc_r: r})

    def _build_anet(self, name, trainable):
        with tf.variable_scope(name):

            split_car = tf.layers.conv1d(self.tfs[:, 0:1, :], 64, 1, strides = 1, activation=tf.nn.tanh)
            split_obs = tf.layers.conv1d(self.tfs[:, 1:2, :], 64, 1, strides = 1, activation=tf.nn.tanh)
            split_goal = tf.layers.dense(self.tfs[:, 2:3, 0:2], 64, tf.nn.tanh)

            split_car_flat = tf.layers.flatten(split_car)
            split_obs_flat = tf.layers.flatten(split_obs)
            split_goal_flat = tf.layers.flatten(split_goal)

            merge_net = tf.keras.layers.concatenate([split_car_flat, split_obs_flat, split_goal_flat])

            input_net = tf.layers.dense(merge_net, 128, tf.nn.tanh)

            a_w = tf.glorot_uniform_initializer()
            mu = 2 * tf.layers.dense(input_net, A_DIM, tf.nn.tanh, kernel_initializer = a_w, trainable=trainable)
            sigma = tf.layers.dense(input_net, A_DIM, tf.nn.softplus, kernel_initializer = a_w, trainable=trainable) + 1e-4

            norm_dist = tf.distributions.Normal(loc = mu, scale = sigma, validate_args= True)

        params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=name)
        return norm_dist, params

    def choose_action(self, s):
        s = s[np.newaxis, :]    
        a = self.sess.run(self.sample_op, {self.tfs: s})[0]

        mu = self.sess.run(self.get_mu, {self.tfs: s})
        sigma = self.sess.run(self.get_sigma, {self.tfs: s})
        self.logger.info('mu is')
        self.logger.info(mu)
        self.logger.info('sigma is')
        self.logger.info(sigma)

        return a

    def get_v(self, s):
        # if s.ndim < 2: 
        s = s[np.newaxis, :]
        return self.sess.run(self.v, {self.tfs: s})[0, 0]
    
    def save(self, TRAIN_TIME):
        dir_path = '/home/xyw/BUAA/Graduation/src/scout/result/multi/model/PPO_%i.ckpt' %(TRAIN_TIME)
        self.saver.save(self.sess, dir_path)
    
    def restore(self, TRAIN_TIME):
        model_path = '/home/xyw/BUAA/Graduation/src/scout/result/multi/model/PPO_%i.ckpt' %(TRAIN_TIME)
        meta_path = model_path + '.meta'
        if os.path.exists(meta_path):
            self.saver = tf.train.import_meta_graph(meta_path)
            self.saver.restore(self.sess, model_path)
        else:
            print('No pre-trained model exist')

    def resetgraph(self):
        tf.reset_default_graph()
