import time
from structures.graphe_md import GrapheMD
from algos.algo_ppp import algo_ppp
from algos.opt_ppp import opt_ppp
from algos.opt_prim import opt_prim
from algos.hds import hds
from plot import afficher_comparaison , afficher_graphe_complet
import utils


def main():
    print("=== PROJET TSP : Comparaison et Visualisation ===")
    
    # 1. Configuration
    N = 10  # Nombre de villes
    
    # Génération
    print(f"Génération de {N} villes...")
    points = utils.generer_points_aleatoires(N)
    graphe = GrapheMD(N, points)

    print("Affichage du graphe complet...")
    afficher_graphe_complet(graphe)

    # Définition des algos (Nom, Fonction lambda)
    # Note : Pour OptPPP, on doit d'abord calculer PPP
    algos = [
        ("PPP (Glouton)", lambda g: algo_ppp(g)),
        ("OptPPP (2-Opt)", lambda g: opt_ppp(algo_ppp(g), g)),
        ("OptPrim (MST)", lambda g: opt_prim(g)),
        ("HDS (Exact)", lambda g: hds(g))
    ]

    donnees_graphiques = [] # Pour stocker les résultats

    print(f"\n{'-'*60}")
    print(f"{'ALGORITHME':<20} | {'COÛT':<15} | {'TEMPS (ms)':<10}")
    print(f"{'-'*60}")

    meilleur_cout_global = float('inf')

    # 2. Exécution des algos
    for nom, fonction in algos:
        start_time = time.time()
        try:
            cycle = fonction(graphe)
            end_time = time.time()
            duree = (end_time - start_time) * 1000
            
            cout = utils.calculer_longueur_cycle(cycle, graphe)
            
            print(f"{nom:<20} | {cout:<15.4f} | {duree:<10.4f}")
            
            # On sauvegarde le résultat pour le plot
            donnees_graphiques.append((nom, cycle, cout))
            
            if cout < meilleur_cout_global:
                meilleur_cout_global = cout
                
        except Exception as e:
            print(f"{nom:<20} | ERREUR: {e}")

    print(f"{'-'*60}")
    
    # 3. Résumé texte
    print("\nRésumé des performances :")
    for nom, cycle, cout in donnees_graphiques:
        diff = ((cout - meilleur_cout_global) / meilleur_cout_global) * 100
        etat = "OPTIMAL" if diff == 0 else f"+{diff:.2f}%"
        print(f" -> {nom} : {etat}")

    # 4. Affichage Graphique
    print("\nLancement de l'affichage graphique...")
    afficher_comparaison(points, donnees_graphiques)

if __name__ == "__main__":
    main()