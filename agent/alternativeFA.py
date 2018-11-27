"""
I'm copying the implementation from

https://github.com/ShangtongZhang/reinforcement-learning-an-introduction/blob/master/chapter10/mountain_car.py
and maybe looking at
https://github.com/ShangtongZhang/reinforcement-learning-an-introduction/blob/master/chapter09/random_walk.py

"""

#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import numpy as np
import matplotlib

N_STATES = 8*18 # manually set

STATES = np.arange(1, N_STATES + 1)

END_STATES = [0, N_STATES + 1]

ACTIONS = range(10)

class IHT:
    "Structure to handle collisions"
    def __init__(self, size_val):
        self.size = size_val
        self.overfull_count = 0
        self.dictionary = {}

    def count(self):
        return len(self.dictionary)

    def full(self):
        return len(self.dictionary) >= self.size

    def get_index(self, obj, read_only=False):
        d = self.dictionary
        if obj in d:
            return d[obj]
        elif read_only:
            return None
        size = self.size
        count = self.count()
        if count >= size:
            if self.overfull_count == 0: print('IHT full, starting to allow collisions')
            self.overfull_count += 1
            return hash(obj) % self.size
        else:
            d[obj] = count
        return count

def hash_coords(coordinates, m, read_only=False):
    if isinstance(m, IHT): return m.get_index(tuple(coordinates), read_only)
    if isinstance(m, int): return hash(tuple(coordinates)) % m
    if m is None: return coordinates

def tiles(iht_or_size, num_tilings, floats, ints=None, read_only=False):
    """returns num-tilings tile indices corresponding to the floats and ints"""
    if ints is None:
        ints = []
    qfloats = [floor(f * num_tilings) for f in floats]
    tiles = []
    for tiling in range(num_tilings):
        tilingX2 = tiling * 2
        coords = [tiling]
        b = tiling
        for q in qfloats:
            coords.append((q + b) // num_tilings)
            b += tilingX2
        coords.extend(ints)
        tiles.append(hash_coords(coords, iht_or_size, read_only))
    return tiles

ACTIONS = range(10)

POSITION_MIN = 0.0
POSITION_MAX = 18.0
EPSILON = 0.4

# wrapper class for state action value function
class ValueFunction:
    # In this example I use the tiling software instead of implementing standard tiling by myself
    # One important thing is that tiling is only a map from (state, action) to a series of indices
    # It doesn't matter whether the indices have meaning, only if this map satisfy some property
    # View the following webpage for more information
    # http://incompleteideas.net/sutton/tiles/tiles3.html
    # @max_size: the maximum # of indices
    def __init__(self, step_size, num_of_tilings=8, max_size=2048):
        self.max_size = max_size
        self.num_of_tilings = num_of_tilings

        # divide step size equally to each tiling
        self.step_size = step_size / num_of_tilings

        self.hash_table = IHT(max_size)

        # weight for each tile
        self.weights = np.zeros(max_size)

        # position and velocity needs scaling to satisfy the tile software
        self.position_scale = self.num_of_tilings / (POSITION_MAX - POSITION_MIN)
        #self.velocity_scale = self.num_of_tilings / (VELOCITY_MAX - VELOCITY_MIN)

    # get indices of active tiles for given state and action
    def get_active_tiles(self, position, action):
        # I think positionScale * (position - position_min) would be a good normalization.
        # However positionScale * position_min is a constant, so it's ok to ignore it.
        active_tiles = tiles(self.hash_table, self.num_of_tilings,
                            [self.position_scale * position],
                            [action])
        return active_tiles

    # estimate the value of given state and action
    def value(self, position, action):
        if position == POSITION_MAX:
            return 0.0
        active_tiles = self.get_active_tiles(position, action)
        return np.sum(self.weights[active_tiles])

    # learn with given state, action and target
    def learn(self, position, action, target):
        active_tiles = self.get_active_tiles(position, action)
        estimation = np.sum(self.weights[active_tiles])
        delta = self.step_size * (target - estimation)
        for active_tile in active_tiles:
            self.weights[active_tile] += delta

    # get # of steps to reach the goal under current state value function
    def cost_to_go(self, position):
        costs = []
        for action in ACTIONS:
            costs.append(self.value(position, action))
    return -np.max(costs)


# get action at @position and @velocity based on epsilon greedy policy and @valueFunction
class BetterFunctionApprox(aBase.Agent):

    def __init__(self, N_action, pre_train_steps, action_per_agent, N_state, encoders, alph==0.1, gam=0, debug=False, test=False):
        super().__init__(pre_train_steps, debug, test)
        self.N_action = N_action
        self.N_state = N_state
        self.score = 0
        self.test = test

    def __enter__(self):
        # probably have memory management here
        print("__enter__ sarsaCentralised")

        return

    def __exit__(self, type, value, tb):
        # have memory management here
        print("__exit__ sarsaCentralised")
        return

    def reset(self):
        # TODO
        return

    def predict(self, state, total_steps, e):
        ### WARNING I've commented out a - 1 at the end that i dont understand!
        randomChoice = super().isRandomGuess(total_steps, e)
        
        if randomChoice:
            action = np.random.randint(0,self.N_action)
        else:
            value_function = self.value_function 
            values = []
            for action in ACTIONS:
                values.append(value_function.value(state, action))
            action = np.random.choice([action_ for action_, value_ in enumerate(values) if value_ == np.max(values)])# - 1
        return action 

    def update(self, last_state, last_action, current_state, is_finished, reward, next_action = 0):
        self.score += reward
        self.value_function.learn(positions[update_time], velocities[update_time], actions[update_time], returns)




