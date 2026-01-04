import time
from structures.graphe_md import GrapheMD
from algos.algo_ppp import algo_ppp
from algos.opt_ppp import opt_ppp
from algos.opt_prim import opt_prim
from algos.hds import hds
import utils


def main():
    print("=== PROJET TSP : Comparaison des Algorithmes ===")
    
    # 1. Configuration
    N = 10  # Nombre de villes (Attention : HDS est lent > 15 villes)
    
    # Génération des points et du graphe
    print(f"Génération de {N} villes...")
    points = utils.generer_points_aleatoires(N)
    graphe = GrapheMD(N, points) # GrapheMD calcule la matrice D automatiquement

    # Liste des algos à tester
    algos = [
        ("PPP (Glouton)", lambda g: algo_ppp(g)),
        ("OptPPP (2-Opt)", lambda g: opt_ppp(algo_ppp(g), g)), # OptPPP prend un cycle initial (celui de PPP)
        ("OptPrim (MST)", lambda g: opt_prim(g)),
        ("HDS (Exact)", lambda g: hds(g))
    ]

    resultats = []

    print(f"\n{'-'*60}")
    print(f"{'ALGORITHME':<20} | {'COÛT':<15} | {'TEMPS (ms)':<10}")
    print(f"{'-'*60}")

    meilleur_cout_global = float('inf')

    for nom, fonction in algos:
        start_time = time.time()
        try:
            # Exécution
            cycle = fonction(graphe)
            
            end_time = time.time()
            duree = (end_time - start_time) * 1000 # ms
            
            # Calcul du coût
            cout = utils.calculer_longueur_cycle(cycle, graphe)
            
            print(f"{nom:<20} | {cout:<15.4f} | {duree:<10.4f}")
            
            resultats.append((nom, cout))
            if cout < meilleur_cout_global:
                meilleur_cout_global = cout
                
        except Exception as e:
            print(f"{nom:<20} | ERREUR: {e}")

    print(f"{'-'*60}")
    
    # Conclusion
    print("\nRésumé des performances :")
    for nom, cout in resultats:
        diff = ((cout - meilleur_cout_global) / meilleur_cout_global) * 100
        etat = "OPTIMAL" if diff == 0 else f"+{diff:.2f}%"
        print(f" -> {nom} : {etat}")

if __name__ == "__main__":
    main()