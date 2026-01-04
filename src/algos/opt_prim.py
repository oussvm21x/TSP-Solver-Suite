from structures.graphe_md import GrapheMD
from structures.graphe_tl import GrapheTL 
from structures.tas import Tas 
from utils import dfs , pi_vers_graphe_tl , prim


# Algorithme d'approximation par Prim pour le problème du voyageur de commerce (TSP)
def opt_prim(G):
    """
    Implémente l'algorithme d'approximation par Prim pour le TSP
    Principe : 

    1. Construire un arbre couvrant de poids minimal (MST) à l'aide de l'algorithme de Prim (pi)
    2. Convertir pi en un GrapheTL représentant l'arbre couvrant
    3. Effectuer un parcours en profondeur (DFS) de l'arbre pour obtenir un cycle hamiltonien approximatif

    Args:
        G (GrapheMD): Le graphe des distances entre les points
    
    Returns:
        list: Une liste représentant le cycle hamiltonien trouvé
    """
  
    # 1. Construire l'arbre couvrant de poids minimal (MST) 
    pi = prim(G) 

    # 2. Convertir pi en GrapheTL
    arbre_mst = pi_vers_graphe_tl(pi)

    # 3. Effectuer un parcours en profondeur (DFS) de l'arbre pour obtenir un cycle hamiltonien approximatif
    P , S , P_star , S_star , pi_dfs = dfs(arbre_mst)

    # P_star contient le cycle hamiltonien approximatif
    return P_star

    

