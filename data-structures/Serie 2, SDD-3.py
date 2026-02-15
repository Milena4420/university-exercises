#!/usr/bin/env python
# coding: utf-8

# # Série 2
# Ce document contient les différents exercices à réaliser. Veuillez compléter et rendre ces exercices dans trois semaines.
# 
# Pour chaque exercice:
# * implémentez ce qui est demandé
# * commentez votre code
# * expliquez **en français** ce que vous avez codé dans la cellule correspondante
# 
# Dans vos explications à chacun des exercices, indiquez un pourcentage subjectif d'investissement de chaque membre du groupe. **Des interrogations aléatoires en classe pourront être réalisées pour vérifier votre contribution/compréhension.**

# ## Exercice 1
# Implémentez et testez un algorithme permettant d'inverser une liste d'entiers en utilisant une méthode récursive.

# In[ ]:


def inverse(m):
    if len(m)<= 1:
        return m
    else:
        return inverse(m[1:] + [m[0]])
    return None


# In[ ]:


assert inverse([5,8,7,3,2]) == [2,3,7,8,5]
assert not inverse([5,8,7,3,2]) == [5,8,7,3,2]


# ### Explications

# Cette fonction prend en paramètre une liste et en retourne son inverse. 
# Si elle est vide ou ne contient qu'un élément, on retourne celui-ci. Sinon, on fait un appel récursif en utilisant une nouvelle liste: on déplace l'élément se trouvant à l'indice 0 à la fin de la liste. 

# ## Exercice 2
# Implémentez une méthode récursive qui trouve et retourne le plus petit élément d'une liste, où la liste et sa taille sont données en paramètre.

# In[7]:


def minEl(m, s: int):
    if s == 1:
        return m[0]
    minimum = minEl(m,s-1)
    if m[s-1]<minimum:
        return m[s-1]
    else: 
        return minimum
    
    return None

# print(minEl([6,5,3,9,1], 5))
# print(minEl([6,5,3,-9,1], 5))


# In[3]:


assert minEl([6,5,3,9,1], 5) == 1
assert minEl([6,5,3,-9,1], 5) == -9
assert not minEl([6,5,3,-9,1], 5) == 1


# ### Explications

# La fonction prend en paramètre une liste ainsi que sa longueur. Si la liste ne contient qu'un élément, c'est le minimum. Sinon, on fais un appel récursif sur la même liste mais en ignorant le dernier élément. La récursivité se poursuit jusqu'à ce que la longeur soit de 1, ce qui initalise le minimum comme étant le premier élément de la liste. Ensuite, en "remontant" les appels récursifs, la fonction compare à chaque étape le dernier élément considéré avec le minimum trouvé jusque-là, et conserve le plus petit. Cela retourne le minimum de la liste une fois que tout les appels soient faits. 

# ## Exercice 3
# Implémentez une méthode récursive qui cherche un élément dans une liste triée en utilisant la recherche binaire. La liste, la taille et l'élément cible sont donnés en paramètre.

# In[11]:


def findItem(m, s: int, t: int):
    if s==0:
        return -1
    mid = s//2 
    if m[mid]==t:
        return mid
    elif t<m[mid]:
        return findItem(m[:mid], mid, t)
    else:
        res = findItem(m[mid+1:], s-mid-1, t)
        if res == -1:
            return -1
        else:
            return mid+1+res
        
    return None

# print(findItem([1,2,4,7,8], 5, 7))
# print(findItem([-12,-9,10,44,85,91], 6, -9))


# In[ ]:


assert findItem([1,2,4,7,8], 5, 7) == 3
assert findItem([-12,-9,10,44,85,91], 6, -9) == 1
assert not findItem([2,4,7,9], 4, 2) == 1


# ### Explications

# La fonction prend en paramètre une liste triée, sa longueur ainsi que l'élément à chercher. Pour commencer, on prend la division entière pour trouver le milieu. Si l'élément est plus petit que celui du milieu, on fait un appel récursif en ne regardant que la partie gauche de la liste. Sinon, on fait un appel récursif en ne regardant que la partie droite de la liste (en faisant attention de "mettre à jour" les indices). Si l'élément a été trouvé, on retourne l'indice auquel il se trouve. Si la liste est vide ou que l'élément n'a pas été trouvé, on retourne -1.

# ## Exercice 4
# La "Fonction 91 de McCarthy" est définie comme suit:
# 
#     M(n) for integers > 0:
#       if n > 100, M(n) = n - 10
#       if n <= 100, M(n) = M(M(n+11))
# 
# La notation `M(M(n+11))` est un appel récursif imbriqué.
# 
# Implémentez et testez une méthode python qui retourne la nombre de McCarthy.

# In[1]:


def mcCarthy(n: int):
    if n<=0:
        return -1
    elif n>100:
        return n-10
    else:
        return mcCarthy(mcCarthy(n+11))
    return None

# pour l'exercice 4.1
#print(mcCarthy(1)) 
#print(mcCarthy(15))
#print(mcCarthy(79))
#print(mcCarthy(99))
#print(mcCarthy(100))
#print(mcCarthy(101))
#print(mcCarthy(200))


# In[ ]:


assert mcCarthy(91) == 91
assert mcCarthy(101) == 91
assert mcCarthy(102) == 92
assert mcCarthy(104) == 94


# ### Explications

# La fonction prend en paramètre et retourne un nombre entier. 
# Si il est négatif: c'est impossible donc retourne -1. 
# Si il est plus grand que 100: retourne n-10.
# Si il est entre 1 et 100: fait un appel récursif imbriqué avec n+11 en paramètre.
# 

# ### Exercise 4.1
# Quels sont les nombres de McCarthy pour: 1, 15, 79, 99, 100, 101, 200 ?

# Dans la cellule où se trouve la fonction, les tests ont été faits. On trouve mcCarthy(1) = mcCarthy(15)= mcCarthy(79) = mcCarthy(99) = mcCarthy(100) = mcCarthy(101) = 91, mcCarthy(200) = 190

# ## Exercice 5 - (<font color='#db60cf'>Bonus</font>) Complexité algorithmique de Fibonacci récursif
# On définit l'*algorithme de Fibonacci récursif* comme suit :

# In[ ]:


def fibonacci_recursive(n):
    global call_counts
    call_counts = call_counts + 1
    if n <= 1:
        return n
    else:
        result1 = fibonacci_recursive(n-1,)
        result2 = fibonacci_recursive(n-2,)
        return result1 + result2  # Summation counts for 1 in the complexity


# Soit $T(n)$ la complexité temporelle de la fonction Fibonacci lorsqu'elle est appelée avec un $n\in \mathbb{N}$. Il vient de l'implémentation que $T(0)=T(1)=1$ et $$T(n)=T(n-1)+T(n-2)+1$$ pour tout $n>1$.
# 
# En admettant que pour tout $n>2$, $T(n-2) \approx T(n-1)$ (en réalité, $T(n-2)=O(T(n-1)$), exprimer $T(n)$ en fonction de $T(n-1)$.
# Exprimer alors $T(n-1)$ en fonction de $T(n-2)$, puis $T(n-2)$ en fonction de $T(n-3)$. Enfin, exprimer $T(n)$ en fonction de $T(n-3)$.
# 
# Démontrer par récurrence une expression de $T(n)$ en fonction de $n$. L'implémenter dans la cellule contenant `def T(n)`.

# Fait sur papier, voir PDF envoyé sur moodle.
# 

# In[ ]:


# Rendering latex equations with a package installed by magic cell
get_ipython().run_line_magic('pip', 'install latexify-py==0.2.0')


# In[6]:


import latexify

@latexify.function
def T(n):
    if n == 0:
        return 1 
    if n == 1:
        return 1
    return (2 **(n))


# Ajouter une ligne à `fibonacci_recursive` pour que le troisième subplot (voir ci-après) montre les valeurs appropriées :

# In[ ]:


call_counts = 0

def fibonacci_recursive(n):
    global call_counts
    call_counts = call_counts + 1
    if n <= 1:
        return n
    else:
        result1 = fibonacci_recursive(n-1,)
        result2 = fibonacci_recursive(n-2,)
        return result1 + result2


# ### Explications

# il faut tout simplement rajouter un compteur qui permet de calculer le nombre de fois que la fonction va être appelée pour calculer le nième terme.

# In[2]:


import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def T(n):
    if n == 0:
        return 1 
    if n == 1:
        return 1
    return (2 **(n))

def measure_execution_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

call_counts = 0

def fibonacci_recursive(n):
    global call_counts
    call_counts = call_counts + 1
    if n <= 1:
        return n
    else:
        result1 = fibonacci_recursive(n-1,)
        result2 = fibonacci_recursive(n-2,)
        return result1 + result2

# Generate values for n
n_values = np.arange(1, 30)

# Lists to store results
execution_times = []
time_complexity_values = []
recursive_calls = []

# Measure execution time, compute time complexity, and count recursive calls for each n
for n in n_values:
    call_counts = 0
    _, execution_time = measure_execution_time(fibonacci_recursive, n)
    time_complexity = T(n)
    execution_times.append(execution_time)
    time_complexity_values.append(time_complexity)
    recursive_calls.append(call_counts)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(n_values, execution_times, label='Execution Time')
plt.xlabel('Input Size (n)')
plt.ylabel('Execution Time (s)')
plt.title('Algorithm Execution Time')

plt.subplot(1, 3, 2)
plt.plot(n_values, time_complexity_values, label='T(n)', color='red', linestyle='dashed')
plt.xlabel('Input Size (n)')
plt.ylabel('Time Complexity')
plt.legend()
plt.title('Time Complexity Function')

plt.subplot(1, 3, 3)
plt.plot(n_values, recursive_calls, label='Recursive Calls')
plt.xlabel('Input Size (n)')
plt.ylabel('Number of Recursive Calls')
plt.title('Number of Recursive Calls')

plt.tight_layout()
plt.show()


# Que montrent ces courbes ?

# Le premier graphe nous montre le temps en secondes nécessaires pour calculer le n-ieme terme de la suite de Fibonacci avec une implémentation récursive.
# On observe que le temps d'exécution croît très rapidement avec n. La courbe semble suivre une fonction exponentielle.
# Cette forte croissance peut s'expliquer par une récursivité non optimisée.
# Chaque appel de la fonction génère deux nouveaux appels.
# Ce qui conduit à un nombre total d'appels exponentiels, que nous pouvons observer dans le deuxième graphe et troisième graphe.
# Le deuxième graphe est une approximation du nombre d'appels. 
# Le troisième graphe est le nombre d'appels exactes.
# 

# In[ ]:




