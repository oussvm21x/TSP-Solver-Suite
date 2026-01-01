import numpy as np 
import heapq # For priority queue implementation


# --- STRUCTURE 1 :  GrapheMD (Matrice de Distance) ---

class GrapheMD: 
    """
    Representation d'un graphe pondéré à l'aide d'une matrice de distances.
    Utuliser pour stocker les distances entre les villes.
    """
    """
    Attributes:
        n (int): Nombre de sommets dans le graphe.
        points (list of tuples): Liste des coordonnées (x, y) des sommets.
        D (numpy.ndarray): Matrice de distances entre les sommets.
    
    Methods:
        _cacluler_distance_euclidienne: Calcule la distance euclidienne entre deux points.
    """
    def __init__(self , n , points ) : 
        self.n = n 
        self.points = points 
        self.D = np.zeros((n,n))
        self._calculer_matrice_distances()
    

    def _calculer_distance_euclidienne(self):
        """ Calcule la matrice des distances euclidiennes entre les points. 
        Utilise la formule de la distance euclidienne pour remplir la matrice D.
        La formule est : d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
        """
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    xi , yi = self.points[i]
                    xj , yj = self.points[j]
                    self.D[i][j] = np.sqrt((xi - xj)**2 + (yi - yj)**2)
                else:
                    self.D[i][j] = 0.0

    
