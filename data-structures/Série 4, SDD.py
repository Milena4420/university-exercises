#!/usr/bin/env python
# coding: utf-8

# # Série 4
# Ce document contient les différents exercices à réaliser. Veuillez compléter et rendre ces exercices dans deux semaines.
# 
# Pour chaque exercice:
# * implémentez ce qui est demandé
# * commentez votre code
# * expliquez **en français** ce que vous avez codé dans la cellule correspondante. Le but est de convaincre le TA de votre compréhension de l'exercice.
# 
# Dans vos explications à chacun des exercices, **indiquez** un pourcentage subjectif d'investissement de chaque membre du groupe. **Des interrogations aléatoires en classe pourront être réalisées pour vérifier votre contribution/compréhension.**
# 
# **Prenez soin** de mettre, si vous êtes en groupe, les **prénoms et noms** des membres dans le titre du/des fichier(s) que vous allez rendre.

# ## Exercice 1
# Ecrivez un programme qui interprête une liste d'instructions en RPN (Reverse Polish Notation).
# * Si l'instruction est un entier, ajoutez-la au sommet de la pile.
# * Les opérations + - * / déclenchent un `pop()` des deux derniers nombres de la pile et un `push()` du résultat de l'opération entre ces deux nombres.
# 
# Exemples:
# 
# - ```1 4 - 3 *``` donne comme résultat ```-9```
# 
# - ```3 4 * 6 / 1 2 +``` donne comme résultat ```2 3```
# 
# Votre solution doit utiliser une pile que vous avez implémentée. Elle doit utiliser une liste (tableau) de taille fixe sans pour autant hériter de `List`. Il faut utiliser les fonctions (que vous devez implémenter) suivantes:

# In[9]:


class MyStack:
    def __init__(self, size: int):
        self.pile = [None]*size  #on initialise un tableau vide de la taille choisie
        self.sommet = -1 #on initialise la pile comme étant vide
        self.maximum = size
        pass

    def print(self):
        if self.is_empty():
            print("La pile est vide")
        else: 
            for i in range(self.sommet+1):
                print(self.pile[i], end=" ")
            print()    
        pass

    def size(self):
        return self.sommet+1

    def is_empty(self):
        if self.sommet == -1:
            return True
        else:
            return False

    def push(self, o: int): 
        if self.sommet+1 >= self.maximum:
            raise FullStackException ("La pile est pleine")
        else:
            self.sommet +=1
            self.pile[self.sommet]=o

    def pop(self): 
        if self.is_empty():
            raise VoidStackException("La pile est vide")
        else:
            valeur=self.pile[self.sommet]
            self.pile[self.sommet]= None
            self.sommet -= 1
            return valeur

class Error(Exception):
    pass

class FullStackException(Error):
    pass

class VoidStackException(Error):
    pass


# In[10]:


s = MyStack(3)
assert s.size() == 0
assert s.is_empty() == True
s.push(1)
s.push(4)
s.print()
assert s.size() == 2
assert s.is_empty() == False
assert s.pop() == 4
s.print()
assert s.size() == 1
s.push(3)
s.push(10)
assert s.size() == 3
s.print()
try:
    s.push(12)
    print("Erreur: FullStackException doit être levée durant cette opération")
except FullStackException:
    pass
except:
    print("Erreur: FullStackException doit être levée durant cette opération")
assert s.pop() == 10
assert s.pop() == 3
assert s.pop() == 1
assert s.size() == 0
assert s.is_empty() == True

s = MyStack(3)
s.push(5)
assert s.size() == 1
assert s.is_empty() == False
s.print()
assert s.pop() == 5
assert s.size() == 0
assert s.is_empty() == True
s.print()
try:
    s.pop()
    print("Erreur: VoidStackException doit être levée durant cette opération")
except VoidStackException:
    pass
except:
    print("Erreur: VoidStackException doit être levée durant cette opération")


# In[23]:


def rpn(entry):
    s= MyStack(len(entry))
    for element in entry:
        try:
            s.push(int(element)) #si c'est un nombre, on le met dans la pile
        except ValueError:
            #c'est un opérateur, donc on enlève les deux derniers éléments mis dans la pile
            y= s.pop() 
            x= s.pop() 
            if element =="+":
                s.push(x+y)
            elif element == "-":
                s.push(x-y)
            elif element == "*": 
                s.push(x*y)
            elif element == "/":
                s.push(int(x/y))
        
    return s


# In[28]:


s = rpn(["1","4","-","3","*"])
s.print() # doit être "-9"
s = rpn(["3","4","*","6","/","1","2","+"])
s.print() # doit être "2 3"


# ### Explications

# Pour structurer nos explications, nous allons faire par fonction:
# - def print: le but est d'afficher notre pile. Si elle est vide, on annonce qu'il n'y a rien à afficher. Sinon, on va aller prendre chaque élément se trouvant à la i-ème position de la pile et on l'affiche. Cela les affiche le résultat en ligne et fait un retour à la ligne quand c'est terminé.
# - def size: le but est de voir combien d'éléments se trouve dans notre pile.
# - def is_empty: elle retourne un booléen, True si la pile est vide, False sinon.
# - def push: le but est d'ajouter un élément à la pile. Si elle est déjà pleine, on soulève une exception. Sinon, on "avance le pointeur" à la place suivante et on ajoute la valeur de l'élément à cette emplacement. 
# - def pop: le but est de retirer un élément de la pile. Si elle est déjà vide, on soulève une exception. Sinon, on crée une variable "valeur" qui stocke le dernier élément de la pile afin de le retourner, on vide son emplacement et on "recule le pointeur" à la place précédente. 
# - def rpn: on fait une itération sur tous les éléments de l'entrée donnée. Lorsque c'est un nombre, on l'ajoute simplement à la pile. Si c'est un opérateur, on enlève les deux derniers éléments mis dans la pile et on fait l'opération demandée entre les deux et on ajoute le résultat à la pile.

# ## Exercice 2
# Implémentez et testez une liste doublement chaînée et son itérateur. Implémentez une classe pour la liste et une autre pour son itérateur. Si cela vous aide, vous pouvez utiliser la classe `Node` du cours.

# In[47]:


class DoublyNode:
    def __init__(self, element=None, nextNode=None, preNode=None):
        self.element= element
        self.nextNode = nextNode
        self.preNode = preNode
        
    def getElement(self):
        return self.element
    def getNext(self):
        return self.nextNode
    def getPre(self):
        return self.preNode
    def setElement(self, element):
        self.element = element
    def setNext(self, nextNode):
        self.nextNode = nextNode
    def setPre(self, preNode):
        self.preNode = preNode
        
        
class DoublyLinkedList:
    def __init__ (self):
        self.debut = None
        self.fin = None
        self.taille = 0
    
    def begin(self):
        return DoublyLinkedIterator(self, self.debut)
       
    def end(self):
        return DoublyLinkedIterator(self, self.fin)

    def add(self, e):
        newNode = DoublyNode(e, None, self.fin)
        if self.debut is None:
            self.debut = newNode
        else: 
            self.fin.setNext(newNode)
        self.fin = newNode
        self.taille +=1
        
    def remove(self):
        if self.debut is None:
            raise VoidStackException("La liste est vide")
        else:
            first = self.debut
            valeur = first.getElement()
            self.debut = first.getNext()
            if self.debut is None:
                self.fin = None
            else:
                self.debut.setPre(None)
            self.taille -=1
            return valeur

    def is_empty(self):
        if self.taille ==0:
            return True
        else: return False


class DoublyLinkedIterator:
    def __init__(self, liste, noeud):
        self.liste = liste
        self.noeud = noeud

    def set(self,e):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else:
            self.noeud.setElement(e)

    def get(self):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else:
            return self.noeud.getElement()

    def increment(self):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else: 
            prochain = self.noeud.getNext()
            if prochain is None:
                raise VoidStackException("Le prochain noeud n'existe pas")
            else:
                self.noeud = prochain
                return self

    def decrement(self):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else: 
            precedent = self.noeud.getPre()
            if precedent is None:
                raise VoidStackException("Le précédent noeud n'existe pas")
            else:
                self.noeud = precedent
                return self

    def equals(self,o):
        if (self.liste is o.liste) and (self.noeud is o.noeud):
            return True
        else:
            return False
        
    
class VoidStackException(Exception):
    pass


# In[48]:


dll = DoublyLinkedList()
assert dll.is_empty() == True
dll.add(3)
assert dll.begin().get() == 3
assert dll.is_empty() == False
dll.add(10)
dll.add(9)
assert dll.end().get() == 9

it = dll.begin()
assert it.get() == 3
it = it.increment()
assert it.get() == 10
it = it.decrement()
assert it.equals(dll.begin()) == True
it.set(4)
assert it.get() == 4

assert dll.remove() == 4
assert dll.begin().get() == 10
assert dll.remove() == 10
assert dll.remove() == 9
assert dll.is_empty() == True


# ### Explications

# Nous avons décidé d'ajouter la classe DoublyNode, comme vu en cours mais en ajoutant des fonctions pour le noeud précédent. Comme pour le premier exercice, on va donner des explications par fonction.
# Pour DoublyLinkedList:
# - def begin: elle crée un pointeur sur le premier noeud de la liste
# - def end: elle crée un pointeur sur le dernier noeud de la liste
# - def add: elle permet d'ajouter un élément à la liste. Si elle est initialement vide, le premier élément est celui qu'on ajoute. Sinon, on l'ajoute à la fin de la liste (donc devient le dernier) et on augmente taille de 1. 
# - def remove: elle permet d'enlever un élément de la liste. Si elle est initialement vide, cela lève une exception car on ne peut rien enlever. Sinon, on conserve la valeur du premier élément de la liste dans la variable "valeur" afin de la retourner, et le prochain élément de la liste devient le premier. On met donc le pointeur sur ce "nouveau premier" et on rédruit la taille de la liste de 1. 
# - def is_empty: retourne True si la liste n'existe pas (ne contient rien) et False sinon
# 
# Pour DoublyLinkedIterator:
# - def set: permet de modifier la valeur de l'élément sur lequel le pointeur se trouve.
# - def get: permet de lire la valeur de l'élément sur lequel le pointeur se trouve
# - def increment: permet de bouger le pointeur sur l'élément suivant de la liste
# - def decrement: permet de bouger le pointeur sur l'élément précédent de la liste
# - def equals: permet de vérifier si deux pointeurs pointent exactement le même endroit (même élément) dans la même liste 
# 
# Pour VoidStackException:
# on l'a crée comme pour l'exercice 1, elle permet de lever une exception lorsqu'on essaie d'aller à une position qui n'existe pas dans notre liste.

# ## Exercice 3
# Implémentez et testez une classe qui crée et rempli la liste doublement chaînée créée dans l'exercice 2 avec _n_ nombres aléatoires entre _0_ et _2n_. Utilisez l'implémentation de l'itérateur de l'exercice 2 pour:
# * itérer dans la liste et afficher chaque élément
# * afficher le premier élément de la liste et la position de la première occurence de X dans la liste:
#   *  le cas où X n’est pas présent dans la liste doit être géré avec une exception dédiée `ItemNotFound`
# * itérer la liste à l'envers (du dernier au premier élément) et afficher chaque élément dans l'ordre d'itération
# * retirer chaque occurrence de X de la liste (elle peut contenir des éléments à double)
#   * le cas où X n’est pas présent dans la liste doit être géré avec une exception dédiée `ItemNotFound`

# In[16]:


import random
class DoublyNode:
    def __init__(self, element=None, nextNode=None, preNode=None):
        self.element= element
        self.nextNode = nextNode
        self.preNode = preNode
        
    def getElement(self):
        return self.element
    def getNext(self):
        return self.nextNode
    def getPre(self):
        return self.preNode
    def setElement(self, element):
        self.element = element
    def setNext(self, nextNode):
        self.nextNode = nextNode
    def setPre(self, preNode):
        self.preNode = preNode
        
        
class DoublyLinkedList:
    def __init__ (self):
        self.debut = None
        self.fin = None
        self.taille = 0
    
    def begin(self):
        return DoublyLinkedIterator(self, self.debut)
       
    def end(self):
        return DoublyLinkedIterator(self, self.fin)

    def add(self, e):
        newNode = DoublyNode(e, None, self.fin)
        if self.debut is None:
            self.debut = newNode
        else: 
            self.fin.setNext(newNode)
        self.fin = newNode
        self.taille +=1
        
    def remove(self):
        if self.debut is None:
            raise VoidStackException("La liste est vide")
        else:
            first = self.debut
            valeur = first.getElement()
            self.debut = first.getNext()
            if self.debut is None:
                self.fin = None
            else:
                self.debut.setPre(None)
            self.taille -=1
            return valeur

    def is_empty(self):
        if self.taille ==0:
            return True
        else: return False


class DoublyLinkedIterator:
    def __init__(self, liste, noeud):
        self.liste = liste
        self.noeud = noeud

    def set(self,e):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else:
            self.noeud.setElement(e)

    def get(self):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else:
            return self.noeud.getElement()

    def increment(self):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else: 
            prochain = self.noeud.getNext()
            if prochain is None:
                raise VoidStackException("Le prochain noeud n'existe pas")
            else:
                self.noeud = prochain
                return self

    def decrement(self):
        if self.noeud is None:
            raise VoidStackException("Le noeud n'existe pas")
        else: 
            precedent = self.noeud.getPre()
            if precedent is None:
                raise VoidStackException("Le précédent noeud n'existe pas")
            else:
                self.noeud = precedent
                return self

    def equals(self,o):
        if (self.liste is o.liste) and (self.noeud is o.noeud):
            return True
        else:
            return False
        
    
class VoidStackException(Exception):
    pass
    
class TestLinkedList:
    
    def __init__(self, n: int):
        self.list = DoublyLinkedList()
        if n >= 1:
            for k in range(n):
                element = random.randint(0, 2*n)
                self.list.add(element)
                
    def first_element(self):
            print(self.list.begin().get())
        
    def print_list_forwards(self):
        image = []
        it = self.list.begin()
        while not it.equals(self.list.end()):
            image.append(it.get())
            it.increment()
        image.append(self.list.end().get())
        print(image)
        
    def first_occurence(self, x):
        it = self.list.begin()
        position = 0
        while not it.equals(self.list.end()):
            if it.get() == x:
                return position
            it.increment()
            position += 1
        if self.list.end().get() == x:
            return position
        raise ItemNotFound("cet élément n'est pas dans cette liste")

    def print_list_backwards(self):
        it = self.list.end()
        backward_list = []
        while not it.equals(self.list.begin()):
            backward_list.append(it.get())
            it.decrement()
        backward_list.append(self.list.begin().get())
        print(backward_list)

    def remove_element(self, x):
        it = self.list.begin()
        new_list = DoublyLinkedList()
        while not it.equals(self.list.end()):
            if it.get() != x:
                new_list.add(it.get())
            it.increment()
        if self.list.end().get()!= x:
            new_list.add(self.list.end().get())
        self.list= new_list
            
            
        
class ItemNotFound(Exception):
    pass
    

test = TestLinkedList(5)
it = test.list.begin()
it.increment()

print(test, it.noeud.getElement())
for k in range(2,7):
    test = TestLinkedList(5)
    test.print_list_forwards()
    test.remove_element(test.list.begin().get())
    test.print_list_forwards()
    test.remove_element(test.list.end().get())
    test.print_list_forwards()
    
    print()
    print()
    print()
    print()


# In[9]:


# Quelques tests à titre indicatif
n = 5
test = TestLinkedList(n)
test.print_list_forwards()
print()
test.first_element()
print()
print("Must be the first element of the list (index = 0)")
test.first_occurence(test.list.begin().get())
test.first_occurence(test.list.end().get())

try:
    test.first_occurence(n*2+1)
    print("Error: ItemNotFound exception must be raised")
except ItemNotFound:
    pass
except:
    print("Error: ItemNotFound exception must be raised")

test.print_list_backwards()
print()
test.remove_element(test.list.begin().get())
test.print_list_forwards()
test.remove_element(test.list.end().get())
test.print_list_forwards()

try:
    test.remove_element(n*2+1)
    print("Error: ItemNotFound exception must be raised")
except ItemNotFound:
    pass
except:
    print("Error: ItemNotFound exception must be raised")


# ### Explications

# La classe TestLinkedList prend en paramètre un entier strictement positif n, qui définit la taille de notre liste doublement chaînée. 
# On génère ensuite n entiers pseudo-aléatoires dans l’ensemble {0, 1, …, 2n}, que l’on ajoute successivement dans cette liste.
# Cette classe contient plusieurs méthodes qui exploitent les fonctions définies précédemment pour manipuler des listes doublement chaînées.
# 
# La méthode first_element permet d’afficher le premier élément de la liste. Pour cela, on place le pointeur sur le nœud de début,puis on extrait et affiche l’élément qu’il contient.
# 
# La méthode print_list_forwards affiche tous les éléments de la liste sous la forme d’une liste Python. On place d’abord le pointeur au début, 
# puis on extrait successivement chaque élément tout en décalant le pointeur vers la droite jusqu’au dernier nœud inclus.
# 
# La méthode first_occurence renvoie la position minimale à laquelle se trouve un élément donné x. Pour cela, on parcourt la liste du début à 
# la fin à l’aide d’un compteur de position. Pour chaque nœud, on compare l’élément à x ; si une correspondance est trouvée,on renvoie la position correspondante. Sinon, on incrémente le compteur et on poursuit le parcours. Une vérification finale permet de s’assurer
# que x est bien présent dans la liste.
# 
# La méthode print_list_backwards affiche la liste à l’envers. On crée une liste vide, puis on parcourt les nœuds de la fin vers le début, en ajoutant à chaque étape l’élément du nœud courant. Il suffit ensuite d’imprimer cette nouvelle liste.
# 
# Enfin, la méthode remove_element permet, pour un élément donné x, de supprimer tous les nœuds dont l’élément est égal à x.
# Pour cela, on crée d’abord une nouvelle liste doublement chaînée vide L. On parcourt ensuite la liste initiale du début à la fin et on ajoute à L uniquement les nœuds dont l’élément est différent de x. À la fin, on remplace la liste initiale par L.

# In[ ]:




