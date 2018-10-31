
import gym
import sklearn.pipeline
import sklearn.preprocessing

env = gym.envs.make("MountainCar-v0")

scaler = sklearn.preprocessing.StandardScaler()


print(env.observation_space.sample())

print(env.reset())