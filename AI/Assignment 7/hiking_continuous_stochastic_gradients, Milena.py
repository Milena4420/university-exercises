#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
np.random.seed(0)


# In[ ]:


# Problem definition (this is not known by the decision maker)

# probabilities for sunny, windy, rainy
weather_distribution = {
    "sunny": 0.41,
    "windy": 0.26,
    "rainy": 0.33
}
weather_conditions = list(weather_distribution.keys())
weather_probs = np.array(list(weather_distribution.values()))
num_weathers = len(weather_distribution)


# In[ ]:



def sunny_utility(water):
    return 7 - (water - 3)**2

def windy_utility(water):
    return 4 - (water - 2)**2

def rainy_utility(water):
    return 2 - (water - 1)**2

optimal_water = {
    "sunny": 2.5,
    "windy": 1.5,
    "rainy": 0.5
}

def get_optimal_action_for(weather):
    return optimal_water[weather]


# In[ ]:


# a simple plot to visualise the actual utility function.
water = np.linspace(0, 5)

sunny_u = sunny_utility(water)
windy_u = windy_utility(water)
rainy_u = rainy_utility(water)

expected_utility = sunny_u * weather_distribution["sunny"] + windy_u * weather_distribution["windy"] + rainy_u * weather_distribution["rainy"] 

plt.grid()
plt.xlabel("Water")
plt.ylabel("Utility")
plt.plot(water, sunny_u, label="Sunny")
plt.plot(water, windy_u, label="Windy")
plt.plot(water, rainy_u, label="Rainy")
plt.plot(water, expected_utility, label="In Expectation")
plt.legend()


# In[ ]:


# TO FILL 
def compute_mse_gradient(observed: float, predicted: float) -> np.ndarray:
    target = np.zeros_like(predicted) #j'ai dû chercher sur internet
    tardget[int(observed)] = 1  #j'ai dû chercher sur internet
    gradient = 2*(predicted-target)
    return gradient

def update_estimate(observed: float, estimate: np.ndarray, learning_rate: float) -> np.ndarray:
    gradient = compute_mse_gradient(observed, estimate)
    new_estimate = estimate - learning_rate * gradient
    total = new_estimate.sum()
    if total>0:
        new_estimate /= total    #je renormalise les estimations
    return new_estimate


# In[2]:


# We want to estimate the amount of water that yields the highest expected utility.
estimate = 0.  # Start with an arbitrary estimate for the best water amount.
num_samples = 10000
learning_rate_schedule = np.linspace(0.01, 0, num_samples)

for i, learning_rate in enumerate(learning_rate_schedule, 1):
    # Sample a random weather condition from the true distribution
    weather = np.random.choice(weather_conditions, p=weather_probs)
    
    if weather == "sunny":
        gradient = -2*estimate +5
    elif weather == "windy":
        gradient = -2*estimate + 3
    elif weather == "rainy":
        gradient = -2*estimate + 1
    estimate += learning_rate*gradient
    #j'ai cherché sur internet la différence entre la manière direct et continue pour pouvoir écrire ça
        
    if i == 1 or i % 500 == 0:
        print("Sampled amount:", i)
        print("Estimates:", estimate)
        print("Estimated best action:", estimate)
    


# In[ ]:




