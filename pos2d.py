"""
Nom : Cherkaoui
Prénom : Jawad
Matricule : 576517
"""


class Pos2D:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.x, self.y}"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y