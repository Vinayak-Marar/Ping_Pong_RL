from environment import PingPong
import pygame
import numpy as np
from lrmodel import LRModel
import matplotlib.pyplot as plt
import pickle
import os

EPSILON = 0.1
ACTION_SPACE = ("L", "R", None)
EPISODES = 5000
ALPHA = 0.01
GAMMA = 0.99

folder = "weights"
if not os.path.exists(folder):
    os.makedirs(folder)

# ------------------------Misc funtions-------------------------------------

def epsilon_greedy(model, state, eps=EPSILON):
    if np.random.random() < eps:
        np.random.choice(ACTION_SPACE)
    else:
        values = model.predict_all_action(state)
        return ACTION_SPACE[np.argmax(values)]
    
#------------------------------------------------------------

env = PingPong(fps=150)
model = LRModel(env)
total_rewards = []

for i in range(EPISODES):

    if i%25 == 0:
        with open(f"weights/weights_{i}.pkl", "wb") as f:
            pickle.dump(model.w, f)

    state = env.reset()
    done = False
    episode_reward = 0

    print(f"episode : {i}")

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
        
        g = model.grad(state, action)
        err = target - model.predict(state, action)
        model.w += ALPHA*err*g

        episode_reward += reward

        state =next_state
        
        # if i % 10 == 0:
        #     env.fps = 60
        #     env.render()
        #     env.fps = 150

    total_rewards.append(episode_reward)

pygame.quit()

plt.plot(total_rewards)
plt.title("Total Rewards")
plt.show()