"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
But : Représentation d'un rectangle défini par deux points.
"""

# importation des modules :
from pos2d import Pos2D


class Box:

    def __init__(self, up_left: Pos2D, down_right: Pos2D) -> None:
        """
        Construction de la représentation à travers plusieurs position.
        """
        self.point1 = up_left     # coin supérieur gauche
        self.point2 = down_right  # coin inférieur droit
        # directions
        self.right = down_right.x
        self.down = down_right.y
        self.left = up_left.x
        self.up = up_left.y
        # edges / bords
        self.edges = self._edges()
 

    def __repr__(self) -> str:
        """
        Renvoie une représentation de l'instance sous la forme point1 point2.
        Utile lors d'un débuggage.
        """
        return f"{self.point1} {self.point2}"


    def width(self) -> tuple[int, int]:
        """
        Renvoie la largeur du rectangle.
        """
        return self.point1.x, self.point2.x


    def height(self) -> tuple[int, int]:
        """
        Renvoie la hauteur du rectangle.
        """
        return self.point1.y, self.point2.y


    # ----- FONCTIONS HELPER ----- 


    def _edges(self) -> list[list[Pos2D]]:
        """
        Renvoie une liste avec les bords du rectangle.
        """
        edges = [[], [], [], []]
        for i in range(self.up + 1, self.down):     # parcours les lignes verticales
            edges[0].append(Pos2D(self.left, i))        # ajout du bord gauche
            edges[1].append(Pos2D(self.right, i))       # ajout du bord droit
        for j in range(self.left + 1, self.right):  # parcours les lignes horizontales
            edges[2].append(Pos2D(j, self.up))          # ajout du bord supérieur
            edges[3].append(Pos2D(j, self.down))        # ajout du bord inférieur
        return edges