#!/usr/bin/env python
# coding: utf-8

# # Série 1
# Ce document contient les différents exercices à réaliser. Veuillez compléter et rendre ces exercices pour dans deux semaines.
# 
# Pour chaque exercice:
# * implémentez ce qui est demandé
# * commentez votre code
# * expliquez **en français** ce que vous avez codé dans la cellule correspondante
# 
# Dans vos explications à chacun des exercices, indiquez un pourcentage subjectif d'investissement de chaque membre du groupe. **Des interrogations aléatoires en classe pourront être réalisées pour vérifier votre contribution/compréhension.**

# ## Exercice 1
# Le PGCD (plus grand commun diviseur) est le plus grand nombre entier qui divise simultanément deux autres nombres entiers.
# 
# Implémentez l'algorithme d'Euclide permettant de calculer le PGCD de deux nombres entiers. Vous trouverez plus d'informations concernant l'algorithme d'Euclide en cliquant sur ce [lien](https://en.wikipedia.org/wiki/Greatest_common_divisor#Euclid's_algorithm).

# In[1]:


def gcd(n: int, m: int):
    result = 0
    while m != 0:
        n, m = m, n%m
       
        result = n
    return result


# In[2]:


assert gcd(9,6) == 3
assert gcd(24,32) == 8
assert gcd(18,18) == 18
assert not gcd(10,15) == 10
assert not gcd(12,9) == 4
assert not gcd(14,14) == 34


# ### Explications

# C'est une fonction qui prend 2 entiers en entrée et qui en retourne un, qui sera leur PGDC. On initie result à 0 et on implémente une boucle while: tant que m ne vaut pas 0, n devient m et m devient le reste de la division euclidienne de n par m. La fonction nous renvoie result=n lorsqu'un nombre a été trouvé, 0 s'il n'y en a aucun.

# ## Exercice 2
# Implémentez une manière de calculer $x^n$ en utilisant la méthode de dichotomie.

# In[ ]:


def powdi(x: int, n: int):
    if n == 0:
        return 1
    if n == 1:
        return x
    if n % 2 == 0:
        return powdi(x, n/2) * powdi(x, n/2)
    if n % 2 != 0:
        return x * powdi(x, n//2) * powdi(x, n//2)
    return None


# In[ ]:


assert powdi(2,3) == 8
assert powdi(4,2) == 16
assert powdi(2,2) == 4
assert powdi(4,0) == 1
assert powdi(2,1) == 2
assert not powdi(5,2) == 10
assert not powdi(3,7) == 10
assert not powdi(3,3) == 10


# ### Explications

# C'est une fonction qui prend 2 entiers en entrée et qui en retourne un, qui est x^n. La fonction est divisée en 4 cas:
# lorsque  n=0: x^0=1 donc on retourne 1
# lorsque n=1: x^1=x donc on retourne x
# lorsque n est pair: on fait 2 appels récursifs avec x^(n/2) car x^n = x^(n/2)* x^(n/2) 
# lorsque n est impair: on fait 2 appels récursifs avec x^(n//2) car x^n = x* x^(n//2)* x^(n//2)


# ## Exercice 3
# La suite de Fibonacci est une suite de nombres entiers dans laquelle chaque nombre $f_{n+2}$ correspond à la somme des deux nombres qui le précèdent, $f_{n+1}+f_{n}$.
# 
# Implémentez l'algorithme de Fibonacci en utilisant la multiplication matricielle.

# In[1]:


import numpy as np

def fibo(n: int):
    f0f1 = np.array([[0],[1]])
    A = np.array([[0,1],
                  [1,1]])
    Apower_n = np.linalg.matrix_power(A, n) # utiliser powdi est preferable !!!
    print(Apower_n)
    return (Apower_n @ f0f1)[0]


# In[ ]:


fibo(8)


# In[6]:


def powdi(x: int, n: int):
    if n == 0:
        return np.identity(2)
    if n == 1:
        return x
    if n % 2 == 0:
        return powdi(x, n/2) @ powdi(x, n/2)
    if n % 2 != 0:
        return x @ powdi(x, n//2) @ powdi(x, n//2)
    return None


# In[8]:


powdi(np.array([[0,1],[1,1]]), 8)


# In[ ]:


assert fibo(8) == 21
assert fibo(10) == 55
assert fibo(0) == 0
assert fibo(1) == 1
assert not fibo(5) == 10


# ### Explications

# Avec le résultat du point 3.1.1, on peut comprendre que pour avoir le n-ième terme de la suite de Fibonnacci, on calcule la matrice A^n avec A [[0,1], [1,1]] puis on effectue la multiplication matricielle par la droite de A^n par le vecteur [f0, f1] = [0, 1].
# On obtient ainsi le vecteur [fn, fn+1] = A^n [f0, f1], comme on l'a démontré au point 3.1.2
# alors il suffit de renvoyer la première coordonnée de ce vecteur, qui est fn.


# ### Exercice 3.1
# $(1)$ Montrez qu'il existe une matrice $A$ reliant $\left[\begin{array}{c}
# f_n \\
# f_{n+1}
# \end{array}\right]$ à $\left[\begin{array}{c}
# f_{n+1} \\
# f_{n+2}
# \end{array}\right]$ pour tout $n\in \mathbb{N}$.
# 
# $(2)$ Trouvez alors une expression de $\left[\begin{array}{c}
# f_n \\
# f_{n+1}
# \end{array}\right]$ selon $A$ et  $\left[\begin{array}{c}
# f_0 \\
# f_{1}
# \end{array}\right]$ .

# (1) soit n un nombre naturel
# soit A une matrice dont les vecteurs colonnes sont [a11, a21] et [a12, a22] i.e A = [[a11, a21], [a12, a22]]
# Supposons que A [fn, fn+1] =  [fn+1, fn+2] 
# On développe le produit matriciel, on a [a11 fn + a12  fn+1, a21 fn + a22 fn+1] = [fn+1, fn+2]
# On a donc les équations a11 fn + a12  fn+1 = fn+1 et  a21 fn + a22 fn+1 = fn+2
# En identifiant les coefficients, on a a12 = a21 = a22 = 1 et a11 = 0
# Donc A = [[0,1], [1,1]]
# 
# (2) On va montrer que pour tout entiers naturels n, on a [fn, fn+1] = A^n [f0, f1] par induction
# Pour l'ancrage, on prend n=1, on a A [f0, f1] = A [0,1] = [1,1] = [f1, f2]
# Pour l'hérédité, On va supposer que pour n arbitraire, on a [fn, fn+1] = A^n [f0, f1]
# Alors pour n+1, par la relation vue au point 1, on a [fn+1, fn+2] = A [fn, fn+1]
# Par hypothèse, A [fn, fn+1] = A A^n [f0, f1] = A^(n+1) [f0, f1]
# Donc [fn+1, fn+2] = A^(n+1) [f0, f1]
# Donc par induction, on a montré que tout entier naturel n, on a [fn, fn+1] = A^n [f0, f1] 


# ### Exercice 3.2 - (<font color='#db60cf'>Bonus</font>) Une formule analytique pour $f_n$
# Que peut-on dire de $A$ ? Déterminez ses valeurs propres et ses sous-espaces propres associés.

# Cherchons les valeurs propres de A
# on calcule det(A - k Id) = k^2 -k -1 = 0 avec Id la matrice identité
# => k1 = (1 + sqrt(5)) / 2 , k2 = (1 - sqrt(5)) / 2 sont les valeurs propres 
# Pour trouver l'espace propre Ek1 associé à k1, on trouve l'ensemble des points [x,y] appartenant à R^2 tel que A [x,y] = k1 [x,y]
# on trouve Ek1 ={[x, k1 x] appartenant à R^2}
# De manière similaire, on trouve l'espace propre associé à k2: Ek2 = {[x, k2 x] appartenant dans R^2}


# En utilisant $(2)$, en déduire une forme analytique de $f_n$.

# On veut déduire une forme analytique de fn
# Grâce au point 3.2, nous savons que A, exprimée dans la base canonique U, est diagonalisable. 
# Donc dans une base V constituée de vecteurs propres, il est facile de calculer B^n, avec B: la matrice A exprimée dans la base V
# On veut utiliser la décomposition A = P B P^(-1)
# Ce qui implique A^n = P B^n P^(-1), avec P la matrice de passage de U vers V
# Prenons V = {[1, k1], [1, k2]}
# A est exprimée dans U la base canonique, donc la matrice de passage P de U à V est P = [[1, k1], [1, k2]]
# Donc P^(-1)= 1/(k1 - k2) [[k2, -k1], [-1, 1]]
# On a donc A^n =  1/(k1-k2) [[k1^n - k2^n, k1^(n+1) - k2^(n+1) ], [k1^(n+1) - k2^(n+1), k1^(n+2) - k2^(n+2)]]
# Donc [fn, fn+1] = A^n [f0, f1] = 1/(k1-k2) [k1^(n+1) - k2^(n+1), k1^(n+2) - k2^(n+2)]
# => fn = (k1^(n+1) - k2^(n+1))/(k1 - k2) 
# ainsi, on obtient notre forme analytique de fn


# ## Exercice 4
# Implémentez et testez les 3 versions de l'algorithme calculant la sous-suite de somme maximale, c'est-à-dire:
# * 3 boucles imbriquées
# * 2 boucles imbriquées
# * une seule boucle (Kadane)

# In[11]:


def maxSub3(m):
    maxSum = 0
    numOps = 0
    n = len(m)
    i = 0
    while (i<n):
        j = i
        while (j<n):
            thisSum = 0
            k = i
            while (k<=j):
                thisSum += m[k]
                k += 1
                numOps += 1
            j += 1
            if (thisSum>maxSum):
                maxSum = thisSum
        i += 1
    return maxSum

def maxSub2(m):
    maxSum = 0
    numOps = 0
    n = len(m)
    for i in range (n):
        j=i
        thisSum=0
        while (j<n):
            thisSum += m[j]
            numOps += 1
            j += 1
            if (thisSum>maxSum):
                maxSum = thisSum
    return maxSum

def maxSub1(m):
    maxSum = 0
    numOps = 0
    n = len(m)
    thisSum = 0
    for i in range (n):
        thisSum += m[i]
        numOps += 1
        if (thisSum>maxSum):
            maxSum = thisSum
        if (thisSum<0):
            thisSum = 0
    return maxSum


# In[12]:


assert maxSub3([4,3,-10,2]) == 7
assert maxSub3([4,3,-10,2,8]) == 10
assert not maxSub3([4,3,-10,2,8]) == -10

assert maxSub2([4,3,-10,2]) == 7
assert maxSub2([4,3,-10,2,8]) == 10
assert not maxSub2([4,3,-10,2,8]) == -10

assert maxSub1([4,3,-10,2]) == 7
assert maxSub1([4,3,-10,2,8]) == 10
assert not maxSub1([4,3,-10,2,8]) == -10


# ### Explications

# maxSub3 calcule toutes les possibilités.
# maxSub2 mémorise certaines valeurs: on prend une sous-suite, puis on lui rajoute un élément à chaque fois.
# maxSub3 ne parcoure qu'une seule fois la liste et ne prend pas en compte les sous-listes qui donne un score négatif.
# Comme vu en cours, l'exercice permet de se rendre compte qu'il existe plusieurs "méthodes" pour résoudre un problème et que certaines demandent plus de temps que d'autres. Plus il y a de boucles, plus cela prend du temps à l'ordinateur. 


# In[ ]:




