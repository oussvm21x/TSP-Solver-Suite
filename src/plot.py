import matplotlib.pyplot as plt

# --- FONCTION D'AFFICHAGE GRAPHIQUE ---
def afficher_comparaison(points, resultats):
    """
    Affiche une grille avec :
    1. Les points initiaux
    2. Le résultat de chaque algorithme
    """
    n_algos = len(resultats)
    # On prévoit 1 plot pour l'initial + n_algos plots
    total_plots = n_algos + 1
    
    # Calcul dynamique des lignes/colonnes (ex: 2 lignes, 3 colonnes)
    cols = 3
    rows = (total_plots // cols) + (1 if total_plots % cols != 0 else 0)
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    # Aplatir le tableau d'axes pour itérer facilement (qu'il soit 1D ou 2D)
    axes = axes.flatten()
    
    # --- PLOT 1 : Configuration Initiale ---
    ax_init = axes[0]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    ax_init.scatter(x, y, c='red', s=50)
    for i, (px, py) in enumerate(points):
        ax_init.annotate(str(i), (px, py), xytext=(5, 5), textcoords='offset points')
    ax_init.set_title(f"Configuration Initiale\n({len(points)} villes)")
    ax_init.set_aspect('equal')

    # --- PLOT 2 à N : Les Algorithmes ---
    for i, (nom, cycle, cout) in enumerate(resultats):
        ax = axes[i + 1] # On commence à l'index 1
        
        # Coordonnées dans l'ordre du cycle
        x_cycle = [points[j][0] for j in cycle]
        y_cycle = [points[j][1] for j in cycle]
        
        # Fermer la boucle
        x_cycle.append(x_cycle[0])
        y_cycle.append(y_cycle[0])
        
        # Dessiner
        ax.plot(x_cycle, y_cycle, 'b-', alpha=0.7) # Lignes bleues
        ax.scatter([p[0] for p in points], [p[1] for p in points], c='red', s=30) # Points rouges
        
        # Numéros
        for idx, (px, py) in enumerate(points):
            ax.annotate(str(idx), (px, py), xytext=(5, 5), textcoords='offset points')
            
        ax.set_title(f"{nom}\nCoût: {cout:.4f}")
        ax.set_aspect('equal')

    # Cacher les axes vides s'il y en a
    for j in range(total_plots, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def afficher_graphe_complet(graphe):
    """
    Affiche le graphe complet avec tous les arcs et leurs coûts.
    Attention : À utiliser seulement pour N petit (<= 10) sinon c'est illisible.
    """
    points = graphe.points
    n = graphe.n
    D = graphe.D
    
    plt.figure(figsize=(10, 10))
    
    # 1. Dessiner toutes les arêtes et les coûts
    # On parcourt la matrice triangulaire supérieure pour ne pas dessiner deux fois
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            cout = D[i][j]
            
            # Dessin de la ligne (arc)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='gray', alpha=0.3, linewidth=0.5)
            
            # Affichage du coût au milieu de l'arête
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            
            # On met le texte sur un fond blanc pour qu'il soit lisible
            plt.text(mid_x, mid_y, f"{cout:.2f}", fontsize=8, color='blue', 
                     ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # 2. Dessiner les sommets
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.scatter(x, y, c='red', s=100, zorder=5)
    
    # 3. Numéroter les villes
    for i, (px, py) in enumerate(points):
        plt.annotate(str(i), (px, py), xytext=(0, 0), textcoords='offset points',
                     ha='center', va='center', color='white', weight='bold')

    plt.title(f"Graphe Complet ({n} villes)\n{n*(n-1)//2} Arcs")
    plt.axis('off') # On cache les axes X/Y pour faire plus propre
    plt.show()


import matplotlib.pyplot as plt

def afficher_comparaison(points, resultats):
    """
    Affiche une grille avec les points initiaux et le résultat de chaque algo.
    """
    n_algos = len(resultats)
    total_plots = n_algos + 1
    
    cols = 3
    rows = (total_plots // cols) + (1 if total_plots % cols != 0 else 0)
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    axes = axes.flatten()
    
    # --- PLOT 1 : Configuration Initiale ---
    ax_init = axes[0]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    ax_init.scatter(x, y, c='red', s=50)
    for i, (px, py) in enumerate(points):
        ax_init.annotate(str(i), (px, py), xytext=(5, 5), textcoords='offset points')
    ax_init.set_title(f"Configuration Initiale\n({len(points)} villes)")
    ax_init.set_aspect('equal')

    # --- PLOT 2 à N : Les Algorithmes ---
    for i, (nom, cycle, cout) in enumerate(resultats):
        ax = axes[i + 1]
        
        x_cycle = [points[j][0] for j in cycle]
        y_cycle = [points[j][1] for j in cycle]
        x_cycle.append(x_cycle[0])
        y_cycle.append(y_cycle[0])
        
        ax.plot(x_cycle, y_cycle, 'b-', alpha=0.7)
        ax.scatter([p[0] for p in points], [p[1] for p in points], c='red', s=30)
        
        for idx, (px, py) in enumerate(points):
            ax.annotate(str(idx), (px, py), xytext=(5, 5), textcoords='offset points')
            
        ax.set_title(f"{nom}\nCoût: {cout:.4f}")
        ax.set_aspect('equal')

    for j in range(total_plots, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

def afficher_graphe_complet(graphe):
    """
    Affiche le graphe complet avec tous les arcs et leurs coûts.
    """
    points = graphe.points
    n = graphe.n
    D = graphe.D
    
    plt.figure(figsize=(10, 10))
    
    # Arêtes
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            cout = D[i][j]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='gray', alpha=0.3, linewidth=0.5)
            
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            plt.text(mid_x, mid_y, f"{cout:.2f}", fontsize=8, color='blue', 
                     ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Sommets
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.scatter(x, y, c='red', s=100, zorder=5)
    
    for i, (px, py) in enumerate(points):
        plt.annotate(str(i), (px, py), xytext=(0, 0), textcoords='offset points',
                     ha='center', va='center', color='white', weight='bold')

    plt.title(f"Graphe Complet ({n} villes)\n{n*(n-1)//2} Arcs")
    plt.axis('off')
    plt.show()