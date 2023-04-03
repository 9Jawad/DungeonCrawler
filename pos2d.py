"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
But : Représente un point avec des coordonnées entières.
"""


class Pos2D:

    def __init__(self, x: int, y: int) -> None:
        """
        Construit un point représentant la position (x, y).
        """
        self.x = x
        self.y = y


    def __repr__(self) -> str:
        """
        Renvoie une représentation de l'instance sous la forme point1.
        Utile lors d'un débuggage.
        """
        return f"{self.x, self.y}"


    def __eq__(self, other) -> bool:
        """
        Renvoie l'égalité entre deux instances via une expression sous la forme point1 == point2.
        """
        return self.x == other.x and self.y == other.y