import numpy as np 
import heapq # For priority queue implementation


# --- STRUCTURE 2 :  GrapheTL (Tableau de Listes d'Adjacence) ---

class GrapheTL:
    """ 
    Representation d'un graphe par liste d'adjacence.
    Utuliser pour stocker l'arbre couvrant minimum (MST) dans OptPrim.
    
    Attributes: 
        n (int): Nombre de sommets dans le graphe.
        T (tableau de listes): Liste d'adjacence représentant le graphe.

    Methods:
        ajouter_arete: Ajoute une arête entre deux sommets avec un poids donné.
        ajouter_arc : Ajoute un arc dirigé entre deux sommets avec un poids donné.
        
    """

    def __init__(self, n):
        self.n = n
        self.T = [[] for _ in range(n)]  # Initialisation du tableau de listes d'adjacence
    
    def ajouter_arete(self, u, v, poids):
        """ Ajoute une arête non dirigée entre les sommets u et v avec le poids spécifié. """
        self.T[u].append((v, poids))
        self.T[v].append((u, poids))

    def ajouter_arc(self, u, v, poids):
        """ Ajoute un arc dirigé de u vers v avec le poids spécifié. """
        self.T[u].append((v, poids))