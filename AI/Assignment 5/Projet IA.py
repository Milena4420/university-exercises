#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
np.random.seed(1)


# In[1]:


# Point 1

actions = {
    "up": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "down": (0, -1),
}

clean = [(0,1)]

def get_adjacent_positions(position: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = position
    return [
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
            (x - 1, y),
    ]

class MowersEnvironment:
    def __init__(self):
        self.start_pos = (0,1)
        self.goal_pos = (0,1)
        self.stone = [(1,0)]
        self.current_position = (0,0)

    def brokemower(self):
        if position in self.stone:
            if np.random.random() < 1/3:
                return True
        return False

    def reset(self):
        """
        Called at the start of the game.
        """
        self.current_position = self.start_pos

    def step(self, action: str) -> Tuple[dict, str, bool]:
        """
        Updates the environment with the action of the agent.
        :returns: new observation for the agent, as well as if the game ended and the outcome.
        """
        act_x, act_y = actions[action]
        curr_x, curr_y = self.current_position

        new_x = curr_x + act_x
        new_y = curr_y + act_y

        
        self.current_position = (new_x, new_y)
        
        if (new_x, new_y) not in clean:
            clean.append((new_x, new_y))

        if self.current_position == self.goal_pos and len(clean) == 4:
            outcome = "finished"
            terminated = True
        elif brokemower(self)==True:
            outcome = "the mower is broken."
            terminated = True

        else:
            outcome = None
            terminated = False

        return  outcome, terminated


# In[ ]:


# Point 2

def random_agent() -> str:
    action_names = list(actions.keys())
    return np.random.choice(action_names)



# In[ ]:


# Point 3-4


class BeliefState:
    
    def __init__(self, initial_stone_belief=0.5):
        self.stone_beliefs = {
            (0, 0): initial_stone_belief,
            (1, 0): initial_stone_belief,
        }  
        self.current_position = (0, 1)

    def update(self, stone: bool, position: Tuple[int, int]):
        self.current_position = position
        new_belief = self.stone_beliefs.copy()

        if position not in self.hole_beliefs:
            continue
        else:   
            if stone==False: 
                if self.stone_beliefs[k] == 0.5:
                    new_belief[k] = 0.4 
                else:
                    new_belief[k] = self.hole_beliefs[k] * 1/3
            # si stone == vrai, la probabilité est de 1 mais
            # automatiquement le jeu s'arrête, donc pas nécessaire.
                
        self.stone_beliefs = new_belief
        
        

