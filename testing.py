import pickle
import numpy as np
from environment import PingPong
from lrmodel import LRModel
import pygame

EPSILON = 0.0
env = PingPong(fps=60)
model = LRModel(env)
GAMMA = 0.95
ACTION_SPACE = ("L", "R", None)

def epsilon_greedy(model, state, eps=EPSILON):
    if np.random.random() < eps:
        np.random.choice(ACTION_SPACE)
    else:
        values = model.predict_all_action(state)
        return ACTION_SPACE[np.argmax(values)]

with open("weights/weights_2025.pkl", "rb") as f:
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