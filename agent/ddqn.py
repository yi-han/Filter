from __future__ import division

import numpy as np
import tensorflow as tf
import os

import itertools

def deep_copy_state(state):
    state_copy = np.empty_like(state)
    state_copy[:] = state
    return state_copy

class Qnetwork():
    def __init__(self, N_state, N_action):
        self.input = tf.placeholder(shape=[None, N_state],dtype=tf.float32)
        self.W_fc1 = tf.Variable(tf.random_uniform([N_state, 256],0,0.01))
        self.b_fc1 = tf.Variable(tf.constant(0.0, shape=[256]))
        self.W_fc2 = tf.Variable(tf.random_uniform([256, 256],0,0.01))
        self.b_fc2 = tf.Variable(tf.constant(0.0, shape=[256]))
        self.W_fc3 = tf.Variable(tf.random_uniform([256, 256],0,0.01))
        self.b_fc3 = tf.Variable(tf.constant(0.0, shape=[256]))
        self.W_out = tf.Variable(tf.random_uniform([256, N_action],0,0.01))
        self.b_out = tf.Variable(tf.constant(0.0, shape=[N_action]))
        self.Qout = tf.add(tf.matmul(tf.nn.relu(tf.add(tf.matmul(tf.nn.relu(tf.add(tf.matmul(tf.nn.relu(tf.add(tf.matmul(self.input, 
                                                                                                                         self.W_fc1), self.b_fc1)), 
                                                                                             self.W_fc2), self.b_fc2)), 
                                                                 self.W_fc3), self.b_fc3)),
                                     self.W_out), self.b_out)
        self.predict = tf.argmax(self.Qout,1)

        #for prioritized experience replay
        self.ISWeights = tf.placeholder(dtype=tf.float32, shape=[None, 1]) #importance sampling weights

        #Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.targetQ = tf.placeholder(shape=[None],dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None],dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions,N_action,dtype=tf.float32)
        
        self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), axis=1)
        
        self.global_step = tf.Variable(0, trainable=False)
        #self.td_error = tf.losses.huber_loss(self.targetQ, self.Q, reduction=tf.losses.Reduction.NONE) #tf.square(self.targetQ - self.Q)
        #self.loss = tf.reduce_max(self.ISWeights * self.td_error) #tf.reduce_mean(self.td_error)

        self.abs_errors = tf.abs(self.targetQ - self.Q)    # for updating Sumtree
        loss = 'squared_difference'
        if loss == 'squared_difference':
            self.loss = tf.reduce_mean(self.ISWeights * tf.squared_difference(self.targetQ, self.Q))
        elif loss == 'linear':
            self.loss = tf.reduce_mean(self.ISWeights * tf.abs(self.targetQ-self.Q))
        elif loss == 'huber':
            # Not sure about this formulation
            self.loss = tf.reduce_mean(self.ISWeights * tf.losses.huber_loss(self.targetQ, self.Q))
        self.gradient_loss_targetQ = tf.gradients(self.loss, [self.targetQ])[0]

        self.rate = tf.train.exponential_decay(0.00005, self.global_step, 1, 0.9999, staircase=True)
        self.trainer = tf.train.AdamOptimizer(learning_rate=tf.maximum(0.000005, self.rate))
        self.updateModel = self.trainer.minimize(self.loss, global_step = self.global_step)

class SumTree(object):
    """
    This SumTree code is modified version and the original code is from: 
    https://github.com/jaara/AI-blog/blob/master/SumTree.py
    Story the data with it priority in tree and data frameworks.
    """
    data_pointer = 0

    def __init__(self, capacity):
        self.capacity = capacity  # for all priority values
        self.tree = np.zeros(2 * capacity - 1)
        # [--------------Parent nodes-------------][-------leaves to recode priority-------]
        #             size: capacity - 1                       size: capacity
        self.data = np.zeros(capacity, dtype=object)  # for all transitions
        # [--------------data frame-------------]
        #             size: capacity

    def add(self, p, data):
        tree_idx = self.data_pointer + self.capacity - 1
        self.data[self.data_pointer] = data  # update data_frame
        self.update(tree_idx, p)  # update tree_frame

        self.data_pointer += 1
        if self.data_pointer >= self.capacity:  # replace when exceed the capacity
            self.data_pointer = 0

    def update(self, tree_idx, p):
        change = p - self.tree[tree_idx]
        self.tree[tree_idx] = p
        # then propagate the change through tree
        while tree_idx != 0:    # this method is faster than the recursive loop in the reference code
            tree_idx = (tree_idx - 1) // 2
            self.tree[tree_idx] += change

    def get_leaf(self, v):
        """
        Tree structure and array storage:
        Tree index:
             0         -> storing priority sum
            / \
          1     2
         / \   / \
        3   4 5   6    -> storing priority for transitions
        Array type for storing:
        [0,1,2,3,4,5,6]
        """
        parent_idx = 0
        while True:     # the while loop is faster than the method in the reference code
            cl_idx = 2 * parent_idx + 1         # this leaf's left and right kids
            cr_idx = cl_idx + 1
            if cl_idx >= len(self.tree):        # reach bottom, end search
                leaf_idx = parent_idx
                break
            else:       # downward search, always search for a higher priority node
                if v <= self.tree[cl_idx]:
                    parent_idx = cl_idx
                else:
                    v -= self.tree[cl_idx]
                    parent_idx = cr_idx

        data_idx = leaf_idx - self.capacity + 1
        return leaf_idx, self.tree[leaf_idx], self.data[data_idx]

    @property
    def total_p(self):
        return self.tree[0]  # the root

class Memory(object):  # stored as ( s, a, r, s_ ) in SumTree
    """
    This SumTree code is modified version and the original code is from:
    https://github.com/jaara/AI-blog/blob/master/Seaquest-DDQN-PER.py
    """
    epsilon = 0.01  # small amount to avoid zero priority
    alpha = 0.6  # [0~1] convert the importance of TD error to priority
    beta = 0.4  # importance-sampling, from initial value increasing to 1
    beta_increment_per_sampling = 0.001
    abs_err_upper = 1.  # clipped abs error

    def __init__(self, capacity):
        self.tree = SumTree(capacity)

    def store(self, transition):
        max_p = np.max(self.tree.tree[-self.tree.capacity:])
        if max_p == 0:
            max_p = self.abs_err_upper
        self.tree.add(max_p, transition)   # set the max p for new p

    def sample(self, n):
        b_idx, ISWeights = np.empty((n,), dtype=np.int32), np.empty((n, 1))
        b_memory = []

        pri_seg = self.tree.total_p / n       # priority segment
        self.beta = np.min([1., self.beta + self.beta_increment_per_sampling])  # max = 1

        min_prob = np.min(self.tree.tree[-self.tree.capacity:][np.nonzero(self.tree.tree[-self.tree.capacity:])]) / self.tree.total_p     # for later calculate ISweight
        for i in range(n):
            a, b = pri_seg * i, pri_seg * (i + 1)
            v = np.random.uniform(a, b)
            idx, p, data = self.tree.get_leaf(v)
            prob = p / self.tree.total_p
            ISWeights[i, 0] = np.power(prob/min_prob, -self.beta)
            b_idx[i] = idx
            b_memory.append(np.array([deep_copy_state(data[0]), data[1], data[2], deep_copy_state(data[3]), data[4], data[5]]))
        return b_idx, np.reshape(b_memory, [n, 6]), ISWeights

    def batch_update(self, tree_idx, abs_errors):
        abs_errors += self.epsilon  # convert to abs and avoid 0
        clipped_errors = np.minimum(abs_errors, self.abs_err_upper)
        ps = np.power(clipped_errors, self.alpha)
        for ti, p in zip(tree_idx, ps):
            self.tree.update(ti, p)

class experience_buffer():
    def __init__(self, buffer_size = 200000):
        self.buffer = []
        self.buffer_size = buffer_size
    
    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)
            
    def sample(self,size):
        return np.reshape(np.array(random.sample(self.buffer,size)),[size,5])

def updateTargetGraph(tfVars,tau):
    total_vars = len(tfVars)
    op_holder = []
    for idx,var in enumerate(tfVars[0:total_vars//2]):
        op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
    return op_holder

def updateTarget(op_holder,sess):
    for op in op_holder:
        sess.run(op)
