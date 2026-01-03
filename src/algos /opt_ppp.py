from structures.graphe_md import GrapheMD

# Version optimisée de l'algorithme du Point Plus Proche (OptPPP)

def opt_ppp(cycle_init, G):
    """
    Implémente une version optimisée de l'algorithme du Point Plus Proche (OptPPP)
    Principe :
        - On cherche a supprimer les croisements dans le cycle hamiltonien
        - Si deux arêtes (A,B) et (C,D) se croisent, on les remplace par (A,C) et (B,D)
          si cela réduit la longueur totale du cycle
    Args:
        cycle_init (list): Une liste représentant le cycle hamiltonien initial
        G (GrapheMD): Le graphe des distances entre les points
    
    Returns:
        list: Une liste représentant le cycle hamiltonien optimisé
    """
    D = G.D 
    n = len(cycle) 
    # Copie du cycle initial , pour ne pas le modifier directement
    cycle = cycle_init.copy()

    amelioration = True

    # Boucle principale de l'optimisation
    while amelioration:
        amelioration = False
        # Parcourir toutes les paires d'arêtes (i, i+1)
        for i in range(n):
            # on la compare avec toutes les arêtes (j, j+1) suivantes
            # j commence a i+2 pour eviter les arêtes adjacentes
            for j in range(i + 2, n):
                # Cas particulier : on ne compare pas la derniere arête avec la premiere
                # car elles sont adjacentes dans le cycle
                # donc si j == n-1 et i == 0 , on saute cette itération
                if i == 0 and j == n - 1:
                    continue

                # Indices des points dans le cycle
                A = cycle[i]
                B = cycle[(i + 1) % n]
                C = cycle[j]
                D = cycle[(j + 1) % n]

                # 1. Calculer les distances
                
                # Calculer la distance actuelle des arêtes (A,B) et (C,D)
                dist_actuelle = G.D[A][B] + G.D[C][D]

                # Calculer la distance si on remplace par (A,C) et (B,D)
                dist_nouvelle = G.D[A][C] + G.D[B][D]

                # 2. Vérifier si le remplacement réduit la distance totale
                if dist_nouvelle < dist_actuelle:
                    # Il y a une amélioration, on effectue le remplacement
                    # Pour cela, on inverse la section du cycle entre B et C
                    cycle[i + 1:j + 1] = reversed(cycle[i + 1:j + 1])
                    amelioration = True

    return cycle