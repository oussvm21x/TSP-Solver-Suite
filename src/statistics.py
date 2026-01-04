import time
import numpy as np
import matplotlib.pyplot as plt
from structures.graphe_md import GrapheMD
import utils
from algos.algo_ppp import algo_ppp
from algos.opt_ppp import opt_ppp
from algos.opt_prim import opt_prim
from algos.hds import hds as algo_hds

def lancer_etude_statistique(N=10, nb_essais=100):
    """
    Exécute 100 essais et calcule les moyennes et pourcentages demandés par le prof.
    Affiche ensuite les graphiques comparatifs (Coût ET Temps).
    """
    print(f"\n=== LANCEMENT DE L'ÉTUDE STATISTIQUE ({nb_essais} essais, N={N}) ===")
    
    # Stockage
    longueurs = {"PPP": [], "OptPPP": [], "OptPrim": [], "HDS": []}
    temps = {"PPP": [], "OptPPP": [], "OptPrim": [], "HDS": []}

    # Boucle des 100 essais
    for i in range(nb_essais):
        if (i+1) % 10 == 0: print(f"Essai {i+1}/{nb_essais}...")
            
        points = utils.generer_points_aleatoires(N)
        graphe = GrapheMD(N, points)

        # 1. PPP
        t0 = time.time()
        c_ppp = algo_ppp(graphe)
        t_ppp = time.time() - t0
        l_ppp = utils.calculer_longueur_cycle(c_ppp, graphe)

        # 2. OptPPP
        t0 = time.time()
        c_optppp = opt_ppp(c_ppp, graphe)
        t_optppp = time.time() - t0 + t_ppp # On ajoute le temps de PPP car OptPPP en dépend
        l_optppp = utils.calculer_longueur_cycle(c_optppp, graphe)

        # 3. OptPrim
        t0 = time.time()
        c_prim = opt_prim(graphe)
        t_prim = time.time() - t0
        l_prim = utils.calculer_longueur_cycle(c_prim, graphe)

        # 4. HDS
        t0 = time.time()
        c_hds = algo_hds(graphe)
        t_hds = time.time() - t0
        l_hds = utils.calculer_longueur_cycle(c_hds, graphe)

        # Enregistrement
        longueurs["PPP"].append(l_ppp)
        longueurs["OptPPP"].append(l_optppp)
        longueurs["OptPrim"].append(l_prim)
        longueurs["HDS"].append(l_hds)
        
        # On stocke les temps en millisecondes (ms) pour l'affichage
        temps["PPP"].append(t_ppp * 1000)
        temps["OptPPP"].append(t_optppp * 1000)
        temps["OptPrim"].append(t_prim * 1000)
        temps["HDS"].append(t_hds * 1000)

    # --- CALCULS STATISTIQUES ---
    moyennes_longueurs = {k: np.mean(v) for k, v in longueurs.items()}
    
    lp, lop, lpr, lmin = moyennes_longueurs["PPP"], moyennes_longueurs["OptPPP"], moyennes_longueurs["OptPrim"], moyennes_longueurs["HDS"]

    # Pourcentages demandés
    gain_optppp = ((lp - lop) / lp) * 100
    gain_prim = ((lop - lpr) / lop) * 100
    ecart_hds = ((lop - lmin) / lmin) * 100

    # --- AFFICHAGE CONSOLE ---
    print(f"\n{'='*65}")
    print(f"RÉSULTATS MOYENS ({nb_essais} essais, N={N})")
    print(f"{'-'*65}")
    print(f"{'ALGO':<10} | {'LONGUEUR':<12} | {'TEMPS (ms)':<12}")
    print(f"{'-'*65}")
    for k in moyennes_longueurs:
        print(f"{k:<10} | {moyennes_longueurs[k]:<12.4f} | {np.mean(temps[k]):<12.4f}")
    print(f"{'='*65}")
    
    print("\nANALYSE :")
    print(f"1. OptPPP améliore PPP de {gain_optppp:.2f}%")
    print(f"2. OptPrim vs OptPPP : {gain_prim:.2f}% (Positif = Prim meilleur)")
    print(f"3. OptPPP est à {ecart_hds:.2f}% de la solution optimale (HDS)")

    # --- GRAPHIQUES STATISTIQUES ---
    plot_stats(longueurs, temps, nb_essais, N)

def plot_stats(longueurs_brutes, temps_bruts, nb_essais, N):
    """
    Génère 4 graphiques : 
    1. Moyenne des longueurs
    2. Moyenne des temps (Log scale)
    3. Distribution des longueurs
    4. Distribution des temps (Log scale)
    """
    
    # Calcul des moyennes pour les bar charts
    algos = list(longueurs_brutes.keys())
    moyennes_longueurs = [np.mean(longueurs_brutes[a]) for a in algos]
    moyennes_temps = [np.mean(temps_bruts[a]) for a in algos]
    
    # Couleurs distinctes pour chaque algo
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

    # Création de la figure 2x2
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Étude Comparative TSP ({nb_essais} essais, N={N})", fontsize=16)

    # --- GRAPHIQUE 1 : Longueurs Moyennes (Bar) ---
    ax1 = axes[0, 0]
    bars1 = ax1.bar(algos, moyennes_longueurs, color=colors, edgecolor='black')
    ax1.set_title("1. Longueur Moyenne des Cycles (Coût)")
    ax1.set_ylabel("Longueur")
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Ajouter les valeurs sur les barres
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # --- GRAPHIQUE 2 : Temps Moyens (Bar - Log Scale) ---
    ax2 = axes[0, 1]
    bars2 = ax2.bar(algos, moyennes_temps, color=colors, edgecolor='black')
    ax2.set_title("2. Temps d'Exécution Moyen (ms)")
    ax2.set_ylabel("Temps (ms) - Échelle Logarithmique")
    
    # !! IMPORTANT : Échelle Log car HDS est trop grand !!
    ax2.set_yscale('log') 
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height * 1.1, # Un peu au dessus
                 f'{height:.2f}', ha='center', va='bottom', fontsize=9)

    # --- GRAPHIQUE 3 : Distribution des Longueurs (Boxplot) ---
    ax3 = axes[1, 0]
    data_longueurs = [longueurs_brutes[a] for a in algos]
    bp1 = ax3.boxplot(data_longueurs, labels=algos, patch_artist=True)
    ax3.set_title("3. Dispersion des Longueurs (Stabilité)")
    ax3.set_ylabel("Longueur")
    ax3.grid(True, linestyle='--', alpha=0.5)
    
    # Coloriage des boites
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)

    # --- GRAPHIQUE 4 : Distribution des Temps (Boxplot - Log Scale) ---
    ax4 = axes[1, 1]
    data_temps = [temps_bruts[a] for a in algos]
    bp2 = ax4.boxplot(data_temps, labels=algos, patch_artist=True)
    ax4.set_title("4. Dispersion des Temps (Performance)")
    ax4.set_ylabel("Temps (ms) - Échelle Logarithmique")
    ax4.set_yscale('log') # Echelle log ici aussi
    ax4.grid(True, linestyle='--', alpha=0.5)

    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()



def etude_evolution_N():
    """
    Lance une étude comparative en faisant varier N (nombre de villes).
    Permet de tracer des courbes d'évolution (Complexité).
    """
    # Liste des tailles à tester (Attention : HDS explose après 14/15)
    # On reste prudent pour que ça ne prenne pas 1 heure.
    liste_N = [5, 7, 9, 11, 12 , 13 ] 
    nb_essais_par_N = 20 # On réduit un peu les essais pour aller vite
    
    print(f"\n=== ÉTUDE D'ÉVOLUTION (N varie : {liste_N}) ===")
    
    # Structures pour stocker les moyennes
    moyennes_temps = {"PPP": [], "OptPPP": [], "OptPrim": [], "HDS": []}
    moyennes_couts = {"PPP": [], "OptPPP": [], "OptPrim": [], "HDS": []}

    for N in liste_N:
        print(f"Traitement N={N}...")
        
        # Accumulateurs temporaires pour ce N
        t_sum = {"PPP": 0, "OptPPP": 0, "OptPrim": 0, "HDS": 0}
        c_sum = {"PPP": 0, "OptPPP": 0, "OptPrim": 0, "HDS": 0}
        
        for _ in range(nb_essais_par_N):
            points = utils.generer_points_aleatoires(N)
            graphe = GrapheMD(N, points)
            
            # PPP
            t0 = time.time()
            c = algo_ppp(graphe)
            dt = time.time() - t0
            l = utils.calculer_longueur_cycle(c, graphe)
            t_sum["PPP"] += dt; c_sum["PPP"] += l
            c_ppp_res = c # Pour OptPPP

            # OptPPP
            t0 = time.time()
            c = opt_ppp(c_ppp_res, graphe)
            dt = time.time() - t0 + (dt) # Temps cumulé
            l = utils.calculer_longueur_cycle(c, graphe)
            t_sum["OptPPP"] += dt; c_sum["OptPPP"] += l

            # OptPrim
            t0 = time.time()
            c = opt_prim(graphe)
            dt = time.time() - t0
            l = utils.calculer_longueur_cycle(c, graphe)
            t_sum["OptPrim"] += dt; c_sum["OptPrim"] += l

            # HDS
            t0 = time.time()
            c = algo_hds(graphe)
            dt = time.time() - t0
            l = utils.calculer_longueur_cycle(c, graphe)
            t_sum["HDS"] += dt; c_sum["HDS"] += l

        # Calcul des moyennes pour ce N
        for k in moyennes_temps:
            moyennes_temps[k].append((t_sum[k] / nb_essais_par_N) * 1000) # en ms
            moyennes_couts[k].append(c_sum[k] / nb_essais_par_N)

    # --- AFFICHAGE GRAPHIQUE (LINE PLOT) ---
    plot_evolution(liste_N, moyennes_couts, moyennes_temps)

def plot_evolution(liste_N, data_couts, data_temps):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Évolution des Performances en fonction de N (Nombre de villes)", fontsize=16)
    
    markers = {'PPP': 'o', 'OptPPP': 's', 'OptPrim': '^', 'HDS': 'D'}
    colors = {'PPP': '#FF9999', 'OptPPP': '#66B2FF', 'OptPrim': '#99FF99', 'HDS': '#FFCC99'}

    # GRAPHE 1 : Évolution du Coût
    for algo, vals in data_couts.items():
        ax1.plot(liste_N, vals, marker=markers[algo], label=algo, color=colors[algo], linewidth=2)
    ax1.set_title("1. Évolution du Coût Moyen")
    ax1.set_xlabel("Nombre de villes (N)")
    ax1.set_ylabel("Longueur moyenne du cycle")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    # GRAPHE 2 : Évolution du Temps (Log scale)
    for algo, vals in data_temps.items():
        ax2.plot(liste_N, vals, marker=markers[algo], label=algo, color=colors[algo], linewidth=2)
    ax2.set_title("2. Évolution du Temps de Calcul")
    ax2.set_xlabel("Nombre de villes (N)")
    ax2.set_ylabel("Temps (ms) - Échelle Log")
    ax2.set_yscale('log') # Indispensable pour voir HDS exploser
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()