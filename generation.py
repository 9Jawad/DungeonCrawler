"""
Nom : Cherkaoui
Prénom : Jawad
Matricule : 576517
"""

# importation des modules :
import argparse
import random
from grid import Grid
from renderer import GridRenderer
##########################


class DungeonGenerator:
    def __init__(self, params: argparse.Namespace) -> None:
        self.parameter = params
        self.board = Grid(params.width, params.height)
        # initialisation du générateur aléatoire
        if params.seed is not None:
            random.seed(params.seed)
    
    def generate(self) -> dict:
        b = self.board
        self.add_rooms()
        # création de l'arbre couvrant en fonction de la difficulté
        self.board = b.spanning_tree() if self.parameter.hard else b.spanning_tree() + b.spanning_tree()
        GridRenderer(self.board).show()
        return {'grid': self.board}
    
    def add_rooms(self) -> None:
        #### paramètres ####
        rooms = self.parameter.rooms
        min_width, min_height = self.parameter.minwidth, self.parameter.minheight
        max_width, max_height = self.parameter.maxwidth, self.parameter.maxheight
        openings = self.parameter.openings
        ####################