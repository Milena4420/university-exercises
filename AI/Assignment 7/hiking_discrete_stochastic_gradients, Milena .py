#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
np.random.seed(0)


# In[ ]:


# Problem definition (this is not known by the decision maker)

# probabilities for sunny, windy, rainy
weather_distribution = np.array([0.41, 0.26, 0.33])
num_weathers = len(weather_distribution)


# In[ ]:


utility_table = np.array(
    # sunny, windy, rainy
    [[10, 5, 0], # no jacket
    [8, 10, 0], # wind breaker
    [5, 5, 10]]  # rain jacket
)
num_actions = len(utility_table)
action_meanings = {
    0: "No Jacket",
    1: "Wind Breaker",
    2: "Rain Jacket"
}


# In[12]:


def compute_optimal_action(estimates: np.ndarray) -> np.ndarray:
    # Pick the optimal action given estimates of the true distribution parameters
    expected_utilities = []
    for action in action_meanings.keys():
        utility = 0
        for weather in range (3):
            utlity += utility_table[action][weather]* estimates[weather]
            expected_utilities.append(utility)
        best_action = np.argmax(expected_utilities)
        best_jacket = action_meanings[best_action]
        return best_jacket


# In[13]:


def compute_mse_gradient(observed: float, predicted: float) -> np.ndarray:
    return (-2)*(observed-predicted)

def update_estimates(observed: float, estimates: np.ndarray, learning_rate: float) -> np.ndarray:
    # update our estimates by taking a gradient step
    pass
    gradient = compute_mse_gradient(observed, estimates)
    new_estimates = estimates - learning_rate*gradient
    total = new_estimates.sum()
    if total>0:
        new_estimates /= total    #je renormalise les estimations
    return new_estimates


# In[ ]:


# We want to estimate the expected utility of picking each jacket.
# Initialise jacket expected utility estimates
estimates = np.ones(num_actions)  # Start with arbitrary estimates
num_samples = 10000
learning_rate_schedule = np.linspace(0.01, 0, num_samples)

for i, learning_rate in enumerate(learning_rate_schedule, 1):
    # Sample a random weather condition from the true distribution
    weather = np.random.choice(num_weathers, p=weather_distribution) 
    
    observed = np.zeros(num_weathers)
    observed[weather]=1
    estimates = update_estimates(observed, estimates, learning_rate)
    
    if i == 1 or i % 500 == 0:
        print("Sampled amount:", i)
        print("Estimates:", estimates)
        print("Estimated best action:", action_meanings[compute_optimal_action(estimates)])
    

