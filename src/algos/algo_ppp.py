from structures.graphe_md import GrapheMD 


# Algorithme du Point Plus Proche (PPP)

def algo_ppp(G):
    """
    Implémente l'algorithme du Point Plus Proche (PPP)
    Principe : 

    1. Partir d'un cycle trivial ( le point 0 et son plus proche voisin)
    2. Tant qu'il reste des villes a visiter : 
        - Selectionner la ville Qi , non encore visitee , la plus proche de cycle courant C 
        - Soit Qj le point de C le plus proche de Qi 
        - Inserer Qi dans C juste a cote de Qj , soit a gauche ou a droite de Qj 
          en choisissant la position qui minimise l'augmentation de la longueur totale du cycle C

    Args:
        G (GrapheMD): Le graphe des distances entre les points
    
    Returns:
        list: Une liste représentant le cycle hamiltonien trouvé
    """
    n = G.n 
    D = G.D

    # Cas particulier : si le graphe est vide ou contient un seul point
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    # --- 1. Initialisation du cycle avec le point 0 et son plus proche voisin
    cycle = [0]
    non_visites = set(range(1, n))

    # Trouver le plus proche voisin du point 0
    plus_proche_voisin = min(non_visites, key=lambda x: D[0][x])
    cycle.append(plus_proche_voisin)
    non_visites.remove(plus_proche_voisin)

    # --- 2. Boucle principale de l'algorithme PPP
    # Inserer les points restants dans le cycle
    while non_visites:
        # 1. Etape 1 : La selection 
        # Trouver la ville Qi la plus proche du cycle courant 
        # On cherche le coouple (Qi , Qj) tel que :
        #     - Qi appartient a non_visites
        #     - Qj appartient a cycle
        #     - La distance D(Qi , Qj) est minimale
        min_distance = float('inf')
        Qi = -1 
        Qj = -1
        for u in non_visites: 
            for idx , v in enumerate(cycle):
                dist = D[u][v]
                if dist < min_distance : 
                    min_distance = dist
                    Qi = u 
                    Qj = v 
                    Qj_index = idx

        # 2. Etape 2 : L'insertion
        # Inserer Qi dans le cycle C juste a cote de Qj
        # Soit a gauche ou a droite de Qj
        # En choisissant la position qui minimise l'augmentation de la longueur totale du cycle C
        
        # Calculer le cout d'insertion a gauche de Qj
        # Identifier le voisin gauche de Qj dans le cycle
        Qj_gauche_index = (Qj_index - 1) % len(cycle)
        Qj_droite_index = (Qj_index + 1) % len(cycle)

        Qj_gauche = cycle[Qj_gauche_index]
        Qj_droite = cycle[Qj_droite_index]

        # Cout d'insertion a gauche
        cout_gauche = D[Qj_gauche][Qi] + D[Qi][Qj] - D[Qj_gauche][Qj]
        # Cout d'insertion a droite
        cout_droite = D[Qj][Qi] + D[Qi][Qj_droite] - D[Qj][Qj_droite] 

        # Choisir la position qui minimise le cout
        if cout_gauche < cout_droite:
            # Insérer Qi à gauche de Qj
            cycle.insert(Qj_index, Qi)
        else:
            # Insérer Qi à droite de Qj
            cycle.insert(Qj_droite_index, Qi)

        non_visites.remove(Qi)

    return cycle  