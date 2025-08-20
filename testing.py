import pickle
import numpy as np
from environment import PingPong
from lrmodel import LRModel
import pygame
import matplotlib.pyplot as plt

EPSILON = 0.2
env = PingPong(fps=100)
model = LRModel(env)
GAMMA = 0.95
ACTION_SPACE = ("L", "R", "None")

def moving_average(array: list, n: int):
    if n <= 0: raise ValueError("n must be > 0")
    if len(array) < n: return []

    arr = [np.mean(array[:n])]
    for i in range(n, len(array)):
        prev = arr[-1]
        arr.append(prev + (array[i] - prev) / n)
    return arr

def epsilon_greedy(model, state, eps=EPSILON):
    if np.random.random() < eps:
        np.random.choice(ACTION_SPACE)
    else:
        values = model.predict_all_action(state)
        return ACTION_SPACE[np.argmax(values)]

with open("weights_2/weights_38000.pkl", "rb") as f:
    weights = pickle.load(f)
    print(weights)

model.w = weights

state = env.reset()
done = False
episode_reward = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    action = epsilon_greedy(model, state)
    next_state, reward, done = env.step(action)

    if done == True:
        target = reward
    else :
            values = model.predict_all_action(next_state)
            target = reward + GAMMA*np.max(values)
    
    # g = model.grad(state, action)
    # err = target - model.predict(state, action)
    # model.w += ALPHA*err*g

    episode_reward += reward

    state =next_state
    
    env.render()

print(episode_reward)

with open("weights_2/reward_14000.pkl", "rb") as f:
    reward_1 = pickle.load(f)

with open("weights_2/reward_26000.pkl", "rb") as f:
    reward_2 = pickle.load(f)

with open("weights_2/reward_37000.pkl", "rb") as f:
    reward_3 = pickle.load(f)

with open("weights_2/reward_38000.pkl", "rb") as f:
    reward_4 = pickle.load(f)

with open("weights_2/reward_49000.pkl", "rb") as f:
    reward_5 = pickle.load(f)


reward = np.concatenate((reward_1, reward_2, reward_3, reward_4, reward_5))

print(len(reward))
print(np.max(reward))
print(np.argmax(reward))

plt.plot(moving_average(reward, 1000))
plt.show()