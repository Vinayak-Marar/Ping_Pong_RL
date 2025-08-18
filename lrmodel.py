import numpy as np
from sklearn.kernel_approximation import RBFSampler
import pickle
import os

ACTION_SPACE = ("L","R",None)
ACTION2INT = {a: i for i, a in enumerate(ACTION_SPACE)}
INT2ONEHOT = np.eye(len(ACTION_SPACE))
SAMPLE_SIZE = 10000

def one_hot(a):
    return INT2ONEHOT[a]

def merge_state_action(s,a):
    ai = one_hot(ACTION2INT[a])
    return np.concatenate((s,ai))

def gather_sample(env,n=SAMPLE_SIZE):
    samples = []
    for _ in range(n):
        print(f"n {_}")
        s = env.reset()
        done = False

        while not done:
            a = np.random.choice(ACTION_SPACE)
            sa = merge_state_action(s, a)
            samples.append(sa)
            
            next_state, r, done = env.step(a)
            s = next_state
    return samples

class LRModel:
   
    def __init__(self,env):
        if not os.path.exists("samples.pkl"):
            samples = gather_sample(env)
            with open("samples.pkl", "wb") as f:
                pickle.dump(samples, f)

        else:
            with open("samples.pkl","rb") as f:
                samples = pickle.load(f)

        self.featurizer = RBFSampler()
        self.featurizer.fit(samples)
        dims = self.featurizer.n_components

        self.w = np.zeros(dims)

    def predict(self, s, a):
        sa = merge_state_action(s, a)
        x = self.featurizer.transform([sa])[0]
        return x @ self.w
    
    def predict_all_action(self, s):
       return [self.predict(s, a) for a in ACTION_SPACE]

    def grad(self, s, a):
       sa = merge_state_action(s, a)
       x = self.featurizer.transform([sa])[0]
       return x
