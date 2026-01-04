from structures import NoeudExploration
import numpy as np
import heapq

# --- ALGO 4 :  Heuristique de la Demi-Somme  --- 
# Implémente l'algorithme HDS pour le problème du TSP en utilisant Branch and Bound.

# Fonction de calcule de la borne inférieure h(x)
def calculer_borne_hds(graphe_md, chemin , cout_actuel , visited_mask):
    """
    Calcule la borne inférieure h(x) pour un chemin partiel donné 
    Principe :
        1. Dans un cycle parfait , chaque ville a exactement deux arêtes 
        2. Cout ideal = 1/2 * Somme(2 arêtes les moins chères pour chaque ville)

    Args:
        graphe_md (GrapheMD): Le graphe du TSP avec les distances
        chemin (list): Le chemin partiel actuel
        cout_actuel (float): Le coût actuel du chemin partiel
        visited_mask (int): Un masque binaire représentant les villes visitées

    Returns:
        float: La borne inférieure h(x) pour le chemin partiel
    """
    n = graphe_md.n  
    D = graphe_md.D 

    start_noued = chemin[0]
    end_noued = chemin[-1]
    somme_deg = 0
    
    # 1. Les arêtes pour les villes déjà visitées 
    # On ajoute les coûts des arêtes connectant les villes visitées
    # Dans la somme des degres , chaque arret compté deux fois 
    somme_deg += 2 * cout_actuel

    # 2. Les arêtes pour les villes non visitées
    for ville in range(n):
        degre_actuel = 0

        # Si la ville est déjà visitée , on passe
        if (visited_mask >> ville) & 1:
            if ville == start_noued or ville == end_noued:
                degre_actuel = 1 # Chaque extrémité du chemin partiel a une seule arête connectée
            else:
                degre_actuel = 2 # Les autres villes visitées ont déjà deux arêtes connectées

        # Si le sommet a déjà deux arêtes connectées , on passe
        if degre_actuel >= 2:
            continue

        # Trouver les arêtes les moins chères pour cette ville 
        nb_arret_trouver = 2 - degre_actuel 
        min1 , min2 = float('inf') , float('inf')
        for voisin in range(n) : 
            if ville == voisin:
                continue

            # Verifier la validite de voisin
            # ca veut dire , verifier que l'arête n'est pas déjà utilisée dans le chemin partiel
            est_visite = (visited_mask >> voisin) & 1
            est_extrémité = (voisin == start_noued or voisin == end_noued)
            if not est_visite or est_extrémité : 
                dist = D[ville][voisin]
                if dist < min1:
                    min2 = min1
                    min1 = dist
                elif dist < min2:
                    min2 = dist
        
        # Ajouter les arêtes les moins chères trouvées
        if nb_arret_trouver >= 1: 
            somme_deg += min1
        
        if nb_arret_trouver == 2:
            somme_deg += min2
    
    # Calculer et retourner la borne inférieure
    return somme_deg / 2










def hds(graphe_md):
    """

    Algorithme HDS (Heuristique de la Demi-Somme) pour résoudre le problème du TSP
    
    Args:
        graphe_md (GrapheMD): Le graphe du TSP avec les distances
    
    Returns:
        tuple: (meilleur_chemin, cout_minimal)
            meilleur_chemin (list): Le chemin optimal trouvé
    """ 

    n = graphe_md.n
    D = graphe_md.D 

    # 1. Initialisations
    start_noued = 0
    mask_initial = 1 << start_noued  # Masque binaire pour le noeud de départ
    cout_initial = 0 
    chemin_initial = [start_noued]
    borne_initiale = calculer_borne_hds(graphe_md, chemin_initial, cout_initial, mask_initial)
    racine = NoeudExploration(current_city=start_noued,
                              visited_mask=mask_initial,
                              cost=cout_initial,
                              bound=borne_initiale,
                              path=chemin_initial)
    
    tas_priorite = []
    heapq.heappush(tas_priorite, racine)

    cout_minimal = float('inf')
    meilleur_chemin = []

    # Variables de securité pour éviter les boucles infinies
    MAX_ITR = 1000000
    nb_itr = 0    

    # 2. Exploration de l'arbre
    while tas_priorite : 
        # Securite 
        nb_itr += 1
        if nb_itr > MAX_ITR :
            print("Alerte : Nombre maximum d'itérations atteint. Arrêt de l'algorithme HDS.")
            break
            
        # Selectionner le noeud avec la plus petite borne
        noeud = heapq.heappop(tas_priorite)

        # Vérifier si le noeud courant peut mener à une meilleure solution
        # Si la borne est déjà supérieure au coût minimal trouvé, on ignore ce noeud
        # car il ne peut pas conduire à une solution optimale

        if noeud.bound >= cout_minimal:
            continue

        # Vérifier si le chemin est complet
        if len(noeud.path) == n:
            # Fermer le cycle en revenant au noeud de départ
            cout_retour = D[noeud.current_city][start_noued]
            cout_total = noeud.cost + cout_retour

            # si on a trouvé un meilleur chemin
            # Mettre à jour le coût minimal et le meilleur chemin
            if cout_total < cout_minimal:
                cout_minimal = cout_total
                meilleur_chemin = noeud.path
            continue
        
        # Si le chemin n'est pas complet , on génère les noeuds enfants
        # Brancheemnt ( Separation / Branching )
        # Explorer les villes non visitées
        for ville in range(n) : 
            # Vérifier si la ville a déjà été visitée
            if (noeud.visited_mask >> ville) & 1:
                continue

            # Calcul des nouvelles valeurs pour le noeud enfant
            new_cost = noeud.cost + D[noeud.current_city][ville]
            if new_cost >= cout_minimal:
                continue
            new_path = noeud.path + [ville]
            new_visited_mask = noeud.visited_mask | (1 << ville)
            new_bound = calculer_borne_hds(graphe_md, new_path, new_cost, new_visited_mask)

            # Si la nouvelle borne est prometteuse , on ajoute le noeud enfant au tas
            if new_bound < cout_minimal:
                enfant = NoeudExploration(current_city=ville,
                                          visited_mask=new_visited_mask,
                                          cost=new_cost,
                                          bound=new_bound,
                                          path=new_path)
                heapq.heappush(tas_priorite, enfant)

    return meilleur_chemin