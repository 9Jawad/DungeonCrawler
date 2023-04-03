"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
But : Permer de générer un donjon en fonction des paramètres passés en argument.
"""

# importation des modules :
import random
import argparse
from box import Box
from grid import Grid
from pos2d import Pos2D
##########################


class DungeonGenerator:
    
    def __init__(self, params: argparse.Namespace) -> None:
        """
        Récupère les paramètres et initialise la grille.
        """
        self.parameters = params
        self.board = Grid(params.width, params.height)
        if params.seed is not None:   # initialisation du générateur aléatoire
            random.seed(params.seed)
    
    
    def generate(self) -> dict:
        """
        Génère le donjon (avec le bon nombre de pièces,
        d'ouvertures par pièce, en concordance avec le mode difficile, etc.
        et qui renvoie un dictionnaire.
        """
        boxes = self.add_boxes()
        self.add_rooms(boxes)                   # création de l'arbre couvrant en fonction de la difficulté
        self.board = self.board.spanning_tree() if self.parameters.hard else self.board.spanning_tree() + self.board.spanning_tree()
        self.add_openings(boxes)
        items = self.generate_items()
        return {'grid': self.board, 'bonuses': items[0], 'start_position': items[1], 'end_position': items[2], 'ghosts': items[3]}


    # ----- FONCTIONS HELPER ----- 


    def add_boxes(self) -> list[Box]:
        """
        Ajoutes les Box généré dans une liste.
        Conditions : Les pièces générées ne peuvent pas se toucher et doivent en particulier avoir au moins 2 cases entre elles.
                    Cela implique également que deux pièces ne peuvent pas avoir d'intersection. 
                    De plus les pièces ne peuvent pas toucher les bords extérieurs du donjon.
        """
        #### paramètres ####
        rooms = self.parameters.rooms
        min_width, min_height = self.parameters.minwidth, self.parameters.minheight
        max_width, max_height = self.parameters.maxwidth, self.parameters.maxheight
        openings = self.parameters.openings
        ####################
        count = 0
        boxes = []
        for i in range(rooms):
            # on part du principe que les parametres sont cohérents entre eux
            w = random.randint(min_width, max_width)
            h = random.randint(min_height, max_height)
            x = random.randint(1, self.board.width - 2 - w)
            y = random.randint(1, self.board.height - 2 - h)
            # Première boite
            if i == 0:
                boxes.append(Box(Pos2D(x, y), Pos2D(x + w, y + h)))
            # vérifier si la boite est en contact avec une autre
            else:
                contact = True
                while contact:
                    for j in range(len(boxes)):
                        if self.contact_check(boxes[j], Box(Pos2D(x, y), Pos2D(x + w, y + h))):
                            w = random.randint(min_width, max_width)
                            h = random.randint(min_height, max_height)
                            x = random.randint(1, self.board.width - 2 - w)
                            y = random.randint(1, self.board.height - 2 - h)
                            contact = True
                            count += 1
                            break
                        else:
                            contact = False
                    # trouver une position valide
                    if not contact:
                        boxes.append(Box(Pos2D(x, y), Pos2D(x + w, y + h)))
                    # sécurité de boucle infinie
                    elif count > 1000:
                        return boxes
        return boxes
    

    def add_rooms(self, boxes: Box) -> None:
        """
        Ajoute les pièces dans le donjon.
        """
        for box in boxes:
            width = box.width()
            height = box.height()
            for i in range(width[0], width[1]):         # marquer les cases des salles
                for j in range(height[0], height[1]):
                    self.board.marked[i][j] = True
            self.board.isolate_box(box)                 # isoler les salles
    
    
    def add_openings(self, boxes: Box) -> None:
        """
        Ajoute les ouvertures dans les pièces.
        """
        for box in boxes:
            for _ in range(self.parameters.openings):            
                choice = random.randint(0, 3)
                edge = box.edges[choice]
                i = random.randint(0, len(edge) - 1)
                pos = edge[i]
                edge.remove(pos)
                dict = {'0': Pos2D(pos.x - 1, pos.y), '1': Pos2D(pos.x + 1, pos.y), \
                        '2': Pos2D(pos.x, pos.y - 1), '3': Pos2D(pos.x, pos.y + 1)}
                self.board.remove_wall(pos, dict[str(choice)])
    
    
    def contact_check(self, rect1: Box, rect2: Box) -> bool:
        """
        Vérifie si deux Box respectent les conditions de distance.
        """
        cond_1 = rect1.right + 2 >= rect2.left and rect1.left - 2 <= rect2.right
        cond_2 = rect1.down + 2 >= rect2.up and rect1.up - 2 <= rect2.down 
        return True if (cond_1 and cond_2) else False  # valide ? True/False
    

    def generate_items(self, items = [], ghosts = []) -> tuple[list[Pos2D], Pos2D, Pos2D, list[Pos2D]]:
        """
        Génère les bonus, la position de départ, la position d'arrivée et les positions des fantômes en aléatoire.
        """
        while len(items) < self.parameters.bonuses + self.parameters.ghosts + 2:
            x = random.randint(0, self.board.width - 1)
            y = random.randint(0, self.board.height - 1)
            if Pos2D(x, y) not in items:
                items.append(Pos2D(x, y))
                self.board.grid[x][y].bonus = True
        # Position de départ + d'arrivée
        start_position, end_position = items.pop(), items.pop()
        for i in start_position, end_position:
            self.board.grid[i.x][i.y].bonus = False
            setattr(self.board.grid[i.x][i.y], f"{'player' if i == start_position else 'end'}", True)
        # Position des fantômes
        for _ in range(self.parameters.ghosts):
            ghost = items.pop()
            ghosts.append(ghost)
            self.board.grid[ghost.x][ghost.y].bonus = False
            self.board.grid[ghost.x][ghost.y].ghost = True
        return items, start_position, end_position, ghosts