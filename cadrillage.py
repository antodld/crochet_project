import matplotlib.pyplot as plt
import numpy as np

def draw_pix(ax,l,c,col):
    ax.add_patch(plt.Rectangle((c + 0.5 , l + 0.5 ), 1, 1, color=col))


def draw_fig(mat : np.ndarray, width = 1):

    label_size = 10
    # Paramètres du quadrillage
    nombre_de_lignes = mat.shape[0]
    nombre_de_colonnes = mat.shape[1]
    # Créer une figure et un axe
    fig, ax = plt.subplots(figsize=(int(0.25*nombre_de_lignes), int(0.25 * nombre_de_colonnes)))



    print(f"col {nombre_de_colonnes}, row {nombre_de_lignes}")

    # Dessiner les lignes verticales du quadrillage
    for i in range(0, nombre_de_colonnes + 1):
        ax.axvline(i + 0.5 , color='gray', linestyle='solid',linewidth =width )

    # Dessiner les lignes horizontales du quadrillage
    for j in range(0, nombre_de_lignes + 1):
        ax.axhline(j + 0.5 , color='gray', linestyle='solid',linewidth =width )


    for i in range(nombre_de_lignes):
        for j in range(nombre_de_colonnes):
            draw_pix(ax,i,j,mat[i,j]) 

    ax3 = plt.twiny()
    ax3.set_xlim(0.5, nombre_de_lignes + 0.5)
    ax3.set_ylim(0.5, nombre_de_colonnes + 0.5)
    ax3.tick_params(labelsize=label_size)
    ax3.set_xticks(range(1, nombre_de_colonnes + 1))

    ax2 = plt.twinx()
    ax2.set_xlim(0.5, nombre_de_colonnes + 0.5)
    ax2.set_ylim(0.5, nombre_de_lignes + 0.5)
    ax2.tick_params(labelsize=label_size)
    ax2.set_yticks(range(1, nombre_de_lignes + 1))

    # Configurer les limites de l'axe
    ax.set_xlim(0.5, nombre_de_colonnes + 0.5)
    ax.set_ylim(0.5, nombre_de_lignes + 0.5)


    ax.tick_params(labelsize=label_size)
    ax.set_xticks(range(1, nombre_de_colonnes + 1))
    ax.set_yticks(range(1, nombre_de_lignes + 1))

    # ax.set_aspect('equal', adjustable='datalim')
    plt.savefig('crochet.pdf', dpi=100)

    # Afficher le quadrillage
    plt.show()
