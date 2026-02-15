#!/usr/bin/env python
# coding: utf-8

# In[19]:


# Exercice 3.3

import heapq

def ucs(graph, start, goal):
    queue = [(0, start)]
    visited = {start: (0,None)}
    
    while queue:
        (current_cost, current_node) = heapq.heappop(queue)
        if current_node == goal:
            return current_cost
        for neighbor, cost in graph[current_node]:
            total_cost = current_cost + cost
            if neighbor not in visited or total_cost<visited[neighbor][0]:
                visited[neighbor] = (total_cost, current_node)
                heapq.heappush(queue, (total_cost, neighbor))
    return None

graph = {
    'Neuchatel' : [('Yverdon', 20), ('Nyon', 60)],
    'Yverdon': [('Lausanne', 30), ('Nyon', 45)],
    'Nyon': [('Geneve', 20)],
    'Lausanne': [('Geneve', 45)],
    'Geneve': []
    
}

start = 'Neuchatel'
goal = 'Geneve'
result = ucs(graph, start, goal)

if result is not None:
    print ("Le chemin plus rapide dure", result, "minutes.")
    
# j'ai utilisé le site https://www.geeksforgeeks.org/uniform-cost-search-ucs-in-ai/ pour faire cette partie de
# l'exercice. J'ai compris comment fonctionne l'algortihme UCS mais malgré plusieurs tentatives, je n'arrivais pas 
# à faire fonctionner mon programme. J'ai donc adapté l'exemple de ce site pour qu'il colle avec mon exemple.


# In[21]:


# Exercice 2: 

def bfsreverse(graph, start, goal):
    queue = [(start,[start], 0)]
    visited = set ()
    
    while queue:
        queue.sort(reverse = True)
        node, path,cost = queue.pop(0)
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph.get(node, []):
                new_path = path + [neighbor]
                queue.append((neighbor, new_path, cost + weight))
    return None


    
    
graph = {
    'S': [('A', 1), ('B', 1), ('C', 2)],
    'A': [],  
    'B': [('F', 2), ('D', 5)],
    'C': [('D', 2)],
    'D': [('G', 3), ('E', 1)],
    'E': [('G', 4)],
    'G': []  
}

print (bfsreverse(graph, start = 'S', goal = 'G'))


# In[ ]:




