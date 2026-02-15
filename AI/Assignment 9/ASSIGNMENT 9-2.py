#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from collections import defaultdict


# In[52]:


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


# In[53]:


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
                                
        # terminal states
        for action in self.actions():
            for state, reward in [("TERMINAL", 0), ("WEIRD_THING", -100), ("HOLE", -100), ("STAIRS", 0)]:
                # all terminal states are "absorbing" states (you can't escape from them)
                self.P[state, action] = {"TERMINAL": 1}
                self.R[state, action] = reward
        
        for x in range(5):
            for y in range(5):
                for x_w in range(5):
                    for y_w in range(5):
                        for action in self.actions():
                            curr_state = (x, y, x_w, y_w)
                            self.R[curr_state, action] = -1
                            adj = pos_for_action(x, y, action)
                            next_x_w, next_y_w = self.weird_thing_policy(x, y, x_w, y_w)
                            
                            if adj in self.walls:
                                next_x, next_y = x, y
                            else:
                                next_x, next_y = adj

                            next_state = (next_x, next_y, next_x_w, next_y_w)
                            
                            if (next_x, next_y) == (next_x_w, next_y_w):
                                # we encountered the weird thing
                                self.P[curr_state, action]["WEIRD_THING"] = 1.
                            elif (next_x, next_y) in self.holes:
                                # we are moving into a hole tile
                                # 50% to fall and 50% to continue. 
                                self.P[curr_state, action]["HOLE"] = 0.5
                                self.P[curr_state, action][next_state] = 0.5

                            elif (next_x, next_y) == self.stairs:
                                # we are moving into stairs

                                # if the weird thing is also at the stairs, then we lose
                                if (next_x_w, next_y_w) == self.stairs:
                                    self.P[curr_state, action]["WEIRD_THING"] = 1.
                                else:
                                    self.P[curr_state, action]["STAIRS"] = 1.

                            else:
                                # we have 100% chance to move to the next location otherwise
                                # the probability of the next state is just given by the probability of
                                # the weird thing moving
                                self.P[curr_state, action][next_state] = 1.
                                
    def actions(self):
        return ["right", "left", "up", "down"]

    def weird_thing_policy(self, x, y, x_w, y_w):
        if (abs(x-x_w)+abs(y-y_w)) == 1:
            return (x_w, y_w)
        move = (x_w, y_w) #on initialise le mouvement comme étant "ne pas bouger"
        min_dist = float("inf") #on initialise la distance minimum comme étant très grande
        for a in self.actions():
            nx,ny = pos_for_action(x_w, y_w, a)
            if (nx,ny) not in self.walls:
                dist = abs(nx-x) + abs(ny-y)
                if dist < min_dist:
                    min_dist = dist
                    move = (nx,ny)
        return move


# In[54]:


def backwards_inference(mdp: MDP, horizon: int) -> Tuple[List[dict], List[dict]]:
    
    Qs = []
    Vs = []
    
    # Initialize V_T(s) = 0 for all s
    V_tp1 = {s: 0.0 for s in mdp.states()} # V_{t+1}
    Vs.append(V_tp1)

    for t in reversed(range(horizon)):
        Qt = {}
        Vt = {}
        for state in mdp.states():
            max_q = float('-inf')
            for action in mdp.actions():
                r = mdp.rewards(state, action)
                expected_value = 0.0
                for next_state, prob in mdp.transition_probabilities(state, action):
                    expected_value += prob * V_tp1[next_state]
                q_val = r + expected_value
                Qt[state, action] = q_val
                max_q = max(max_q, q_val)
            Vt[state] = max_q
        Qs.insert(0, Qt)
        Vs.insert(0, Vt)
        V_tp1 = Vt
    
    return Qs, Vs


# In[55]:


def compute_policy(mdp: MDP, Qs: List[dict]) -> List[dict]:
    
    policy = []
    
    for Qt in Qs:
        pi_t = {}
        for state in mdp.states():
            best_action = max(mdp.actions(), key=lambda a: Qt[state, a])
            pi_t[state] = best_action
        policy.append(pi_t)
            
    return policy


# In[56]:


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

    # Fill in the heatmap based on fixed weird_thing_pos
    for x in range(5):
        for y in range(5):
            key = (x, y, x_w, y_w)
            if key in Vt:
                heatmap[y, x] = Vt[key]  # Note: y first due to matplotlib row/col format

    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.cm.viridis
    im = ax.imshow(heatmap, cmap=cmap, origin='lower')

    # Gridlines
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

    # Plot agent and weird thing
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


# In[57]:


mdp = DungeonMDP()

T = 25
Qs, Vs = backwards_inference(mdp, T)
policy = compute_policy(mdp, Qs)


# In[62]:


def simulate(Vs, policy, mdp):
        
    idx = 0
    weird_thing_pos = (4, 4) # you can change this to see how the agent reacts to 
    for t in range(1, T+1):
        
        v_pi_heatmap(Vs, policy, t, weird_thing_pos, mdp)
        
simulate(Vs, policy, mdp)
        


# In[ ]:





# In[ ]:




