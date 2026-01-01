import numpy as np
import heapq

# --- STRUCTURE 4 :  Noeud d'Exploration ---

class NoeudExploration:
    """ 
    Representation d'un noeud d'exploration dans l'arboresence de recherche du Branch and Bound.

    Attributes:
        current_city (int): Le sommet actuel dans le chemin.
        visited_mask (int): Un masque binaire représentant les villes visitées.
        cost (float): Le coût g(x) du chemin actuel.
        bound (float): La borne inférieure h(x) pour ce noeud.
        path (list): Le chemin partiel parcouru jusqu'à présent.

    Methods:
        __lt__: Méthode de comparaison pour le tas binaire basée sur la borne.

    """

    def __init__(self, current_city, visited_mask, cost, bound, path):
        self.current_city = current_city # Sommet actuel
        self.visited_mask = visited_mask # Masque des visités
        self.cost = cost                 # Coût g(x)
        self.bound = bound               # Heuristique h(x)
        self.path = path                 # Chemin partiel

    def __lt__(self, other):
        # Comparaison pour le Tas : on priorise la plus petite borne
        return self.bound < other.bound