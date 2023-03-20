"""
Nom : Cherkaoui
Prénom : Jawad
Matricule : 576517
"""

# importation des modules :
from pos2d import Pos2D


class Box:
    def __init__(self, ul: Pos2D, lr: Pos2D):
        self.point1 = ul  # coin supérieur gauche
        self.point2 = lr  #      inférieur droit

    def __repr__(self) -> str:
        return f"Box(width : {self.width()}, height: {self.height()})"

    def width(self) -> tuple[int, int]:
        return self.point1.x, self.point2.x

    def height(self) -> tuple[int, int]:
        return self.point1.y, self.point2.y