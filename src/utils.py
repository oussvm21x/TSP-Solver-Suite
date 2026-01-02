import random 
import os 

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
