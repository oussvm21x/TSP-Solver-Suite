import random 
import os 
import sys 
from structures.tas import Tas 
from structures.graphe_md import GrapheMD
from structures.graphe_tl import GrapheTL 
# --- Helper functions 

# --- 1. Generer des points aleatoires 
def generer_points_aleatoires(n):
    """
    Génère une liste de n points dont les coordonnées (x, y) sont tirées 
    aléatoirement et uniformément dans l'intervalle [0, 1]

    Args:
        n (int): Le nombre de points à générer
    
    Returns:
        list: Une liste de tuples représentant les points générés

    """ 
    points = []
    for _ in range(n):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        points.append((x, y))
    return points

# --- 2. Lire un fichier texte

def lire_fichier_texte(chemin_fichier):
    """
    Lire un fichier de texte contenat des coordonnées de points 
    et retourner une liste de tuples représentant ces points.

    Args:
        chemin_fichier (str): Le chemin vers le fichier texte

    Returns:
        list: Une liste de tuples représentant les points lus du fichier
    """
    points = []
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Le fichier {chemin_fichier} n'existe pas.")
    
    try:
        with open(chemin_fichier, 'r') as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue
                
                # Nettoyage : on enlève parenthèses et virgules pour supporter "(x, y)" et "x y"
                ligne_propre = ligne.replace('(', '').replace(')', '').replace(',', ' ')
                parties = ligne_propre.split()
                
                if len(parties) >= 2:
                    try:
                        x = float(parties[0])
                        y = float(parties[1])
                        points.append((x, y))
                    except ValueError:
                        print(f"Ignoré (format invalide) : {ligne}")
                        continue
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        
    return points

# --- 3. Calculer longeure d'un cycle hamiltonien
def calculer_longueur_cycle(cycle , graphe_md):
    """
    Calcule la longueur totale d'un cycle hamiltonien donné.

    Args:
        cycle (list): Une liste de tuples représentant les points du cycle
        graphe_md (dict): Un dictionnaire représentant le graphe des distances

    Returns:
        float: La longueur totale du cycle
    """
    longueur = 0.0
    n = len(cycle)
    D = graphe_md.D 
    for i in range(n):
        u = cycle[i] 
        v = cycle[(i + 1) % n]  # Prochain point, en bouclant au début
        longueur += D[u][v]
    
    return longueur


# --- 4. DFS 
# Augmentation de la limite de récursion pour les grands graphes
sys.setrecursionlimit(200000)

def dfs(GTL) : 
    """
    Algorithme de parcours en prodondeure (DFS) 
    
    Args : j
        GTL(GrapheTL) : Le graphe à parcourir 

    Returns :
        tuple : (P , S, P_star , S_star , pi)
        P : Ordre de decouverte (Numéro de visite)
        S : Ordre de fin de visite
        P_start : Liste des sommets dans l'ordre de découverte
        S_star : Liste des sommets dans l'ordre de fin de visite
        pi : Tableau des prédécesseurs

    """
    n = GTL.n 

    # Initialisations
    ip = 0  # Indice de prefixe
    is_ = 0  # Indice de suffixe

    couleure = [0] * n  # 0 : blanc , 1 : gris , 2 : noir

    pi = [-1] * n 
    P = [0] * n
    S = [0] * n
    P_star = [0] * n
    S_star = [0] * n

    BLANC , GRIS , NOIR = 0 , 1 , 2 

    # --- Procédure récursive interne
    # visiter en profondeur 
    def visiter_en_profondeur(u) : 
        nonlocal ip , is_

        # Marquer le sommet comme visité (gris) 
        couleure[u] = GRIS 

        # Enregistrer le sommet dans l'ordre de découverte 
        ip += 1 
        P[u] = ip
        P_star[ip - 1] = u

        # On decouvre les voisins 
        voisins = sorted(G.T[u])

        # Boucle principale de la procedure 
        for v in voisins : 
            if couleure[v] == BLANC :
                pi[v] = u 
                visiter_en_profondeur(v) 
        
        # Exploration de u est terminer 
        couleure[u] = NOIR 

        # u est ajouté à l'ordre de fin de visite
        is_ += 1
        S[u] = is_
        S_star[is_ - 1] = u

    # --- Boucle principale de DFS
    for u in range(n) :
        if couleure[u] == BLANC :
            visiter_en_profondeur(u)
    return (P , S , P_star , S_star , pi)



# --- 5. Prim algorithme 
def prim(graphe_md) : 
    """
    Implementation de l'algorithme de Prim pour construire un arbre couvrant de poids minimal (MST)
    Version optimisée utilisant un tas binaire pour la sélection efficace des arêtes de poids minimal.

    Args :
        graphe_md (GrapheMD) : Le graphe des distances entre les points

    Returns :
        list : le tableau des prédécesseurs (pi) représentant le MST construit 
    """
    n = graphe_md.n 
    D = graphe_md.D 

    # Initialisations 
    cle = [float('inf')] * n 
    pi = [-1] * n 
    visite = [False] * n 

    # Initialiser le tas avec les clés 
    F = Tas()
    cle[0] = 0
    F.inserer(0, cle[0])

    while not F.est_vide() :
        # Extraire le sommet u avec la clé minimale 
        s = F.extraire_min()

        if visite[s] :
            continue
        visite[s] = True


        # Mettre à jour les clés des voisins de u 
        for t in range(n) : 
            if s == t :
                continue
            if not visite[t] and D[s][t] < cle[t] :
                cle[t] = D[s][t]
                pi[t] = s 
                F.inserer(t, cle[t])    
    return pi


# --- 6. Convertir pi en GrapheTL
def pi_vers_graphe_tl(pi) :
    """
    Convertit le tableau des prédécesseurs (pi) en un GrapheTL représentant l'arbre couvrant.

    Args :
        pi (list) : Le tableau des prédécesseurs

    Returns :
        GrapheTL : Le graphe représentant l'arbre couvrant
    """
    n = len(pi)
    GTL = GrapheTL(n)

    for v in range(n) :
        u = pi[v]
        if u != -1 :
            GTL.ajouter_arc(u, v)
    
    return GTL