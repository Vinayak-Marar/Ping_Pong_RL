from environment import PingPong
import pygame
import numpy as np
from lrmodel import LRModel
import matplotlib.pyplot as plt
import pickle
import os

EPSILON = 0.1
ACTION_SPACE = ("L", "R", "None")
EPISODES = 50000
ALPHA = 0.1
GAMMA = 0.99

folder = "weights_2"
if not os.path.exists(folder):
    os.makedirs(folder)

# ------------------------Misc funtions-------------------------------------

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
        return np.random.choice(ACTION_SPACE)
    else:
        values = model.predict_all_action(state)
        return ACTION_SPACE[np.argmax(values)]
    
#------------------------------------------------------------

env = PingPong(fps=150)
model = LRModel(env)
with open("weights_2/weights_14000.pkl", "rb") as f:
    weights = pickle.load(f)

model.w = weights

total_rewards = []

for i in range(14001,EPISODES):

    if i%200 == 0:
        with open(f"weights_2/weights_{i}.pkl", "wb") as f:
            pickle.dump(model.w, f)

    eps = 0.1
    if i<10000:
        eps = 0.2
    

    state = env.reset()
    done = False
    episode_reward = 0

    print(f"episode : {i}")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        action = epsilon_greedy(model, state, eps=eps)
        next_state, reward, done = env.step(action)

        if done == True:
            target = reward
        else :
                values = model.predict_all_action(next_state)
                target = reward + GAMMA*np.max(values)
        
        g = model.grad(state, action)
        err = target - model.predict(state, action)
        model.w += ALPHA*err*g

        episode_reward += reward

        state = next_state
        
        # if i % 10 == 0:
        #     env.fps = 60
        #     env.render()
        #     env.fps = 150

    total_rewards.append(episode_reward)
    if i%1000 == 0:
        print(episode_reward)
        with open(f"weights_2/reward_{i}.pkl", "wb") as f:
            pickle.dump(total_rewards, f)


pygame.quit()

plt.plot(total_rewards)
plt.title("Total Rewards")
plt.show()