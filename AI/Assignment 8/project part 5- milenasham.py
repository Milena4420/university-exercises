#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from collections import defaultdict


# In[3]:


class MDP:
    def __init__(self):
        
        self.P = defaultdict(dict)
        self.R = {}
        self._states = None
        
    def states(self):
        if self._states is None:
            self._states = [
                s
            for s, a in self.P.keys()
            ]
        return self._states
    
    def actions(self):
        return []

    def transition_probabilities(self, state, action):
        return self.P[state, action].items()

    def rewards(self, state, action):
        return self.R[state, action]


# In[36]:


def pos_for_action(x, y, action):
    if action == "right":
        return x+1, y
    if action == "left":
        return x-1, y
    if action == "up":
        return x, y+1
    if action == "down":
        return x, y-1

class LawnmowerMDP(MDP):
    
    def __init__(self):
        super().__init__()    
        self.stone = [(3,2)]
        self.refill_base = (0, 0)
        x_d, y_d = 4, 1
        self.dog_path = [(4, 1), (3, 1), (2, 1), (2,2), (2,3), (3,3), (4,3), (4,2)]
        path_length = len(self.dog_path)
        
        for action in self.actions():
            for state, reward in [("TERMINAL", 0), ("DOG", -15), ("STONE", -15), ("DONE", 10)]:
                self.P[state, action] = {"TERMINAL": 1}
                self.R[state, action] = reward
        
        for x in range(5):
            for y in range(5):
                for path_idx in range(path_length):
                    for mowed_set in [frozenset()]:
                        for action in self.actions():
                            adj = pos_for_action(x, y, action) 
                            x_d, y_d = self.dog_path[path_idx]
                            curr_state = (x, y, x_d, y_d, mowed_set)
                            next_mowed = set(mowed_set)
                            reward = -1
                            next_x, next_y = adj
                            
                            if (next_x, next_y)not in next_mowed:
                                next_mowed.add((next_x, next_y))
                                reward += 1
                                
                            next_mowed_frozen = frozenset(next_mowed)
                            self.R[curr_state, action] = reward
                        
                            for d_prob, next_path_idx in self.dog_actions(path_idx):
                                next_x_d, next_y_d = self.dog_path[next_path_idx]
                                
                                next_state = (next_x, next_y, next_x_d, next_y_d, next_mowed_frozen)

                                if (next_x, next_y) in self.stone:
                                    self.P[curr_state, action]["STONE"] = self.P[curr_state, action].get("STONE", 0) + (1/3) * d_prob
                                    self.P[curr_state, action][next_state] = self.P[curr_state, action].get(next_state,0) + (2/3) * d_prob

                                elif (next_x, next_y) == self.refill_base:
                                    if (next_x_d, next_y_d) == self.refill_base:
                                        self.P[curr_state, action]["DOG"] = self.P[curr_state, action].get("DOG",0) + d_prob
                                    else:
                                        self.P[curr_state, action]["REFILL_BASE"] = self.P[curr_state, action].get("REFILL_BASE", 0) + d_prob

                                elif (next_x, next_y) == (next_x_d, next_y_d):
                                    self.P[curr_state, action]["DOG"] = self.P[curr_state, action].get("DOG",0) + d_prob

                                else:
                                    self.P[curr_state, action][next_state] = self.P[curr_state, action].get(next_state,0) + d_prob

    def actions(self):
        return ["right", "left", "up", "down"]

    def dog_actions(self, idx):
        return [
        (0.3, idx), 
        (0.7, (idx+1)%len(self.dog_path)), 
        ]            


# In[30]:


def backwards_induction(mdp: MDP, horizon: int) -> Tuple[List[dict], List[dict]]:
    
    Qs = []
    Vs = []
    
    # Initialize V_T(s) = 0 for all s
    Vtp1 = {s: 0.0 for s in mdp.states()} # V_{t+1}
    Vs.append(Vtp1)

    for t in reversed(range(horizon)):
        Qt = {} 
        Vt = {}
        
        for s in mdp.states(): 
            action_values = {} #dic qui stockera les valeurs Q(s,a) pour chaque a
            for a in mdp.actions():
                q_value = mdp.R[s,a] #r(s,a)
                for s_next, prob in mdp.P[s,a].items():
                    q_value += prob * Vtp1[s_next] # on multiplie P(s'|s,a) avec la futur valeur pondérée
                action_values[a]= q_value
                Qt[(s,a)]= q_value
            Vt[s] = max(action_values.values()) #on choisit la meilleure valeur de Q(s,a)
 
        Qs.insert(0, Qt)
        Vs.insert(0, Vt)
        Vtp1 = Vt
    
    return Qs, Vs


# In[31]:


# Optimal policy computation
def compute_policy(mdp: MDP, Qs: List[dict]) -> List[dict]:
    # This function returns the policy didacted by the given Q function.
    
    policy = []
    
    for Qt in Qs:
        pi_t = {}
        for state in mdp.states():
            best_action = max(mdp.actions(), key=lambda a: Qt[state, a])
            pi_t[state] = best_action
        policy.append(pi_t)
            
    return policy


# In[32]:


# Visualisation utils

action_to_vector = {
    "up": (0, 0.3),
    "down": (0, -0.3),
    "left": (-0.3, 0),
    "right": (0.3, 0),
}

def v_pi_heatmap(Vs, policy, timestep: int, weird_thing_pos: tuple, lawnmower: LawnmowerMDP):
    """
    Plots a heatmap for the value function V at a given timestep.
    
    """
    heatmap = np.full((5, 5), np.nan)
    
    Vt = Vs[timestep]
    pi_t = policy[timestep]
    
    x_d, y_d = dog_pos

    for x in range(5):
        for y in range(5):
            key = (x, y, x_d, y_d)
            if key in Vt:
                heatmap[y, x] = Vt[key]  # Note: y first due to matplotlib row/col format

    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.cm.viridis
    im = ax.imshow(heatmap, cmap=cmap, origin='lower')

    ax.set_xticks(np.arange(5))
    ax.set_yticks(np.arange(5))
    ax.set_xticklabels(range(5))
    ax.set_yticklabels(range(5))
    
    for (x, y) in LawnmowerMDP.stone:
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor='none', edgecolor='red', hatch='O', linewidth=1))

    x, y = LawnmowerMDP.refill_base
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor='none', edgecolor='green', hatch='*', linewidth=1.5))

    ax.plot(x_w, y_w, marker='x', markersize=10, color='red', label="DOG")
    
    for x in range(5):
        for y in range(5):

            key = x, y, x_d, y_d
            if key in pi_t:
                action = pi_t[key]
                dx, dy = action_to_vector[action]
                ax.arrow(x, y, dx, dy, head_width=0.15, head_length=0.1, fc='black', ec='black')

    ax.set_title(f"Value Function and policy at t={timestep}")
    ax.legend(loc='upper right')
    fig.colorbar(im, ax=ax)
    plt.show()


# In[34]:


mdp = LawnmowerMDP()
T = 25
Qs, Vs = backwards_induction(mdp, T)
policy = compute_policy(mdp, Qs)


# In[35]:


# Run this cell to test and visualise the learned policy/Value function
def simulate(Vs, policy, mdp):
        
    idx = 0
    d_pos = mdp.dog_path[idx]
    for t in range(1, T+1):
        
        v_pi_heatmap(Vs, policy, t, d_pos, mdp)
        # simulate weird thing moving
        d_action_dist = mdp.dog_actions(idx)
        idx = np.random.choice([d[1] for d in d_action_dist], p=[d[0] for d in d_action_dist])
        d_pos = mdp.dog_path[idx]

simulate(Vs, policy, mdp)


# In[ ]:




