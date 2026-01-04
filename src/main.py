import os
import sys
from structures.graphe_md import GrapheMD
import utils

# Importation des modules d'affichage et de stats
from plot import afficher_comparaison, afficher_graphe_complet

from statistics import lancer_etude_statistique , etude_evolution_N

# Importation des algorithmes
from algos.algo_ppp import algo_ppp
from algos.opt_ppp import opt_ppp
from algos.opt_prim import opt_prim
from algos.hds import hds as algo_hds

def mode_demo():
    print("\n--- MODE DÉMONSTRATION (Visualisation) ---")
    choix = input("1. Points aléatoires\n2. Fichier texte\nChoix : ")
    
    points = []
    if choix == '2':
        chemin = input("Chemin du fichier (ex: data/exemple.txt) : ")
        if os.path.exists(chemin):
            points = utils.lire_fichier_texte(chemin)
        else:
            print("Fichier introuvable. Génération aléatoire par défaut.")
            points = utils.generer_points_aleatoires(10)
    else:
        try:
            n_val = int(input("Nombre de villes (N) : ") or 10)
        except: n_val = 10
        points = utils.generer_points_aleatoires(n_val)

    # Création du graphe
    graphe = GrapheMD(len(points), points)
    
    # Affichage du graphe complet si N est petit
    if len(points) <= 10:
        print("Affichage du graphe complet...")
        afficher_graphe_complet(graphe)

    # Exécution des algos
    resultats = []
    algos = [
        ("PPP", lambda g: algo_ppp(g)),
        ("OptPPP", lambda g: opt_ppp(algo_ppp(g), g)),
        ("OptPrim", lambda g: opt_prim(g)),
        ("HDS", lambda g: algo_hds(g))
    ]

    print("\nCalcul en cours...")
    for nom, func in algos:
        try:
            c = func(graphe)
            l = utils.calculer_longueur_cycle(c, graphe)
            resultats.append((nom, c, l))
            print(f" -> {nom} terminé (Coût: {l:.4f})")
        except Exception as e:
            print(f"Erreur {nom}: {e}")

    # Affichage final
    afficher_comparaison(points, resultats)

def main():
    while True:
        print("\n=== PROJET TSP : MENU PRINCIPAL ===")
        print("1. Démonstration Visuelle (1 seul graphe)")
        print("2. Étude Statistique (100 essais - Demande Prof)")
        print("3. Étude de l'évolution en fonction de N")
        print("4. Quitter")
        
        choix = input("Votre choix : ")
        
        if choix == '1':
            mode_demo()
        elif choix == '2':
            try:
                N = int(input("Taille des graphes N (conseil: 10) : ") or 10)
                lancer_etude_statistique(N=N, nb_essais=100)
            except ValueError:
                print("Valeur incorrecte.")
        elif choix == '3':
            # Lance la nouvelle fonction
            etude_evolution_N()
        elif choix == '4':
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()