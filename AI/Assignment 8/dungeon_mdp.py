#!/usr/bin/env python
# coding: utf-8

# In[19]:


import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from collections import defaultdict


# In[21]:


class MDP:
    def __init__(self):
        
        # empty transition function
        self.P = defaultdict(dict)
        # empty reward function
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


# In[29]:


def pos_for_action(x, y, action):
    if action == "right":
        return x+1, y
    if action == "left":
        return x-1, y
    if action == "up":
        return x, y+1
    if action == "down":
        return x, y-1

class DungeonMDP(MDP):
    
    def __init__(self):
        super().__init__()    
        self.walls = [
            (0,2), (2,2), (2,3), (2, 0) 
        ]
        for i in range(5):
            self.walls.append((-1, i))
            self.walls.append((5, i))
            self.walls.append((i, -1))
            self.walls.append((i, 5))
        
        self.holes = [
            (0, 4), (3, 2)
        ]
        
        self.stairs = (3, 4)
                
        x_w, y_w = 4, 1
        
        self.weird_thing_path = [
            (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4),
            (4, 4), (4, 3), (4, 2)
        ]
        path_length = len(self.weird_thing_path)
        
        # terminal states
        for action in self.actions():
            for state, reward in [("TERMINAL", 0), ("WEIRD_THING", -100), ("HOLE", -100), ("STAIRS", 0)]:
                self.P[state, action] = {"TERMINAL": 1}
                self.R[state, action] = reward
        
        for x in range(5):
            for y in range(5):
                for path_idx in range(path_length):
                    for action in self.actions():
                        adj = pos_for_action(x, y, action)
                        
                        x_w, y_w = self.weird_thing_path[path_idx]
                        curr_state = (x, y, x_w, y_w)
                        
                        self.R[curr_state, action] = -1
                        
                        for w_prob, next_path_idx in self.weird_thing_actions(path_idx):
                            next_x_w, next_y_w = self.weird_thing_path[next_path_idx]
                            
                            if adj in self.walls:
                                next_x, next_y = x, y
                            else:
                                next_x, next_y = adj
                            
                            # This next state, by default, has w_prob chance to happen given our action
                            next_state = (next_x, next_y, next_x_w, next_y_w)
                            
                            if (next_x, next_y) in self.holes:
                                self.P[curr_state, action]["HOLE"] = self.P[curr_state, action].get("HOLE", 0) + 0.5 * w_prob
                                self.P[curr_state, action][next_state] = self.P[curr_state, action].get(next_state,0) + 0.5 * w_prob

                            elif (next_x, next_y) == self.stairs:
                                if (next_x_w, next_y_w) == self.stairs:
                                    self.P[curr_state, action]["WEIRD_THING"] = self.P[curr_state, action].get("WEIRD_THING",0) + w_prob
                                else:
                                    self.P[curr_state, action]["STAIRS"] = self.P[curr_state, action].get("STAIRS", 0) + w_prob
                            
                            elif (next_x, next_y) == (next_x_w, next_y_w):
                                self.P[curr_state, action]["WEIRD_THING"] = self.P[curr_state, action].get("WEIRD_THING",0) + w_prob
                                
                            else:
                                self.P[curr_state, action][next_state] = self.P[curr_state, action].get(next_state,0) + w_prob
                                
    def actions(self):
        return ["right", "left", "up", "down"]

    def weird_thing_actions(self, idx):
        return [
        (0.05, idx), 
        (0.75, (idx+1)%len(self.weird_thing_path)), 
        (0.20, idx-1)
        ]            


# In[32]:


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


# In[25]:


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


# In[30]:


# Visualisation utils

action_to_vector = {
    "up": (0, 0.3),
    "down": (0, -0.3),
    "left": (-0.3, 0),
    "right": (0.3, 0),
}

def v_pi_heatmap(Vs, policy, timestep: int, weird_thing_pos: tuple, dungeon: DungeonMDP):
    """
    Plots a heatmap for the value function V at a given timestep.
    
    """
    heatmap = np.full((5, 5), np.nan)
    
    Vt = Vs[timestep]
    pi_t = policy[timestep]
    
    x_w, y_w = weird_thing_pos

    for x in range(5):
        for y in range(5):
            key = (x, y, x_w, y_w)
            if key in Vt:
                heatmap[y, x] = Vt[key]  # Note: y first due to matplotlib row/col format

    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.cm.viridis
    im = ax.imshow(heatmap, cmap=cmap, origin='lower')

    ax.set_xticks(np.arange(5))
    ax.set_yticks(np.arange(5))
    ax.set_xticklabels(range(5))
    ax.set_yticklabels(range(5))
    
    for (x, y) in dungeon.walls:
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='black'))

    for (x, y) in dungeon.holes:
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor='none', edgecolor='red', hatch='O', linewidth=1))

    x, y = dungeon.stairs
    ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor='none', edgecolor='green', hatch='*', linewidth=1.5))

    ax.plot(x_w, y_w, marker='x', markersize=10, color='red', label="Weird Thing")
    
    for x in range(5):
        for y in range(5):

            key = x, y, x_w, y_w
            if key in pi_t:
                action = pi_t[key]
                dx, dy = action_to_vector[action]
                ax.arrow(x, y, dx, dy, head_width=0.15, head_length=0.1, fc='black', ec='black')

    ax.set_title(f"Value Function and policy at t={timestep}")
    ax.legend(loc='upper right')
    fig.colorbar(im, ax=ax)
    plt.show()


# In[31]:


mdp = DungeonMDP()
T = 25
Qs, Vs = backwards_induction(mdp, T)
policy = compute_policy(mdp, Qs)


# In[33]:


# Run this cell to test and visualise the learned policy/Value function
def simulate(Vs, policy, mdp):
        
    idx = 0
    w_pos = mdp.weird_thing_path[idx]
    for t in range(1, T+1):
        
        v_pi_heatmap(Vs, policy, t, w_pos, mdp)
        # simulate weird thing moving
        w_action_dist = mdp.weird_thing_actions(idx)
        idx = np.random.choice([d[1] for d in w_action_dist], p=[d[0] for d in w_action_dist])
        w_pos = mdp.weird_thing_path[idx]

simulate(Vs, policy, mdp)


# In[15]:


get_ipython().system('pip install matplotlib')


# In[ ]:




