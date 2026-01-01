import numpy as np
import heapq 

# --- STRUCTURE 3 :  Tas binaire (Min-Heap) ---

class Tas:
    """ 
    Représentation d'un tas binaire (min-heap) pour la gestion efficace des priorités.
    
    Attributes: 
        elements (list): Liste des éléments dans le tas, chaque élément est un tuple (priority, value).
    
    Methods:
        inserer: Insère un nouvel élément dans le tas.
        extraire_min: Extrait et retourne l'élément avec la plus petite priorité.
        est_vide: Vérifie si le tas est vide.
    """

    def __init__(self):
        self.elements = []  # Initialisation de la liste des éléments du tas

    def inserer(self, element , priority):
        """ Insère un nouvel élément dans le tas. """
        heapq.heappush(self.elements, (priority, element))

    def extraire_min(self):
        """ Extrait et retourne l'élément avec la plus petite priorité. """
        return heapq.heappop(self.elements)

    def est_vide(self):
        """ Vérifie si le tas est vide. """
        return len(self.elements) == 0
