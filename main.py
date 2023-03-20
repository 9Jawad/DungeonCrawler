"""
Nom : Cherkaoui
Prénom : Jawad
Matricule : 576517
"""

# importation des modules :
import argparse


def main():
    ##############  CONFIGURATION  ##############
    parse = argparse.ArgumentParser()
    parse.add_argument('width', help="Paramètre obligatoire correspondant à la longueur de la grille sur base de laquelle le donjon va être généré.")
    parse.add_argument('height', help="Paramètre obligatoire correspondant à la hauteur de la grille sur base de laquelle le donjon va être généré.")
    parse.add_argument('--rooms', help="Permet de specifier le nombre (possiblement nul) de pièces à introduire dans le donjon.", required=False, default=5)
    parse.add_argument('--seed', help="Permet de specifier la seed (graine) utilisée pour la génération du donjon, utile pour debugger votre code.", required=False, default=None)
    parse.add_argument('--minwidth', help="Permet de specifier la dimension minimale que peut prendre chacune des pièces qui vont être ajoutées au donjon.", required=False, default=4)
    parse.add_argument('--minheight', help="Permet de specifier la dimension minimale que peut prendre chacune des pièces qui vont être ajoutées au donjon.", required=False, default=4)
    parse.add_argument('--maxwidth', help="Permet de specifier la dimension maximale que peut prendre chacune des pièces qui vont être ajoutées au donjon.", required=False, default=8)
    parse.add_argument('--maxheight', help="Permet de specifier la dimension maximale que peut prendre chacune des pièces qui vont être ajoutées au donjon.", required=False, default=8)
    parse.add_argument('--openings', help="Permet de specifier le nombre d'ouvertures (entrées/sorties) qui sont ajoutées à chaque pièce.", required=False, default=2)
    parse.add_argument('--hard', help="Permet de specifier que le donjon à générer doit être basé sur un labyrinthe et pas sur une union d'arbres couvrants.", required=False)
    parameter = parse.parse_args()


if __name__ == '__main__':
    main()