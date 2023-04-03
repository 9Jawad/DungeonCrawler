"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
But : Représentation de la personne tentant de sortir du donjon.
"""

# importation des modules :
import random
import argparse
from grid import Grid
from pos2d import Pos2D
##########################


class Player:
    
    def __init__(self, board: Grid, dict: dict, params: argparse.Namespace) -> None:
        """
        Construit un joueur et son espace de jeu.
        """
        self.board = board
        # position
        self.pos = dict['start_position']
        self.end = dict['end_position']
        self.bonuses = dict['bonuses']
        self.ghosts = dict['ghosts']
        self.count = 0
        self.count_ = 1
        # radius
        self.bonus = params.bonus_radius
        self.view = params.view_radius
        self.torch = params.torch_delay
        # ghosts
        self.g_delay = params.ghosts_delay
        self.g_mouv = params.ghosts_walls


    def deplacement(self, direction: str) -> str or bool: 
        """
        Á partir de la direction donnée, renvoie la position suivante.
        """
        # initialize
        pos = self.pos
        grid = self.board.grid
        dict = {'z': (Pos2D(pos.x, pos.y - 1), 'up'), 's': (Pos2D(pos.x, pos.y + 1), 'down'), \
                'q': (Pos2D(pos.x - 1, pos.y), 'left'), 'd': (Pos2D(pos.x + 1, pos.y), 'right')}
        next_pos = dict[direction][0]
        attr = dict[direction][1]
        
        # mouvement possible 
        if getattr(grid[pos.x][pos.y], attr):
            
            # --- gestion des items ---
            # Torch 
            if self.count == self.torch:
                self.view -= 1
                self.count = 0
                # Parti Perdu
                if self.view == 0:
                    return "It's so dark in here"
            # Ghosts
            if self.count_ == self.g_delay:
                for i, ghost in enumerate(self.ghosts):
                    dict = {'up': Pos2D(ghost.x, ghost.y - 1), 'down': Pos2D(ghost.x, ghost.y + 1), \
                            'left': Pos2D(ghost.x - 1, ghost.y), 'right': Pos2D(ghost.x + 1, ghost.y)}
                    # ne traverse pas les murs
                    if self.g_mouv:
                        cond = False
                        while not cond:
                            neighbours = self.board.accessible_neighbours(ghost)
                            random.shuffle(neighbours)
                            new_pos = neighbours[0]
                            if self.ghosts_cond(new_pos):
                                self.ghosts_edit_node(ghost, new_pos, i)
                                cond = True
                    else: # traverse les murs
                        cond = False
                        while not cond:
                            key = random.choice(list(dict.keys()))
                            new_pos = dict[key]
                            if self.board.dimension_checker(new_pos) and self.ghosts_cond(new_pos):
                                self.ghosts_edit_node(ghost, new_pos, i)
                                cond = True
                self.count_ = 0    
        
            # --- Cas de déplacement ---
            # Bonus (cas: @)
            if next_pos in self.bonuses: 
                self.view += self.bonus                  # augmente le rayon de vue
                self.bonuses.remove(next_pos)            # suppr le bonus de la liste
                self.edit_node(pos, next_pos, 'bonus')   # modif des nodes + count
            # Parti Gagné (cas: #)
            elif next_pos == self.end:
                self.edit_node(pos, next_pos, 'end')
                return True
            # Parti Perdu (cas: G) 
            elif next_pos in self.ghosts:
                self.edit_node(pos, next_pos, 'ghost')
                return "Ain't you afraid of no ghost ?"
            # Cas de base
            else:
                self.edit_node(pos, next_pos)


    # ----- FONCTIONS HELPER ----- 


    def edit_node(self, pos: Pos2D, next_pos: Pos2D, cas: str=None) -> None:
        """
        Modifie les nodes pour afficher le déplacement du joueur et des items.
        Il fait également l'actualisation de la position courante du joueur. 
        """
        # modifie les nodes
        grid = self.board.grid
        grid[next_pos.x][next_pos.y].player = True
        grid[pos.x][pos.y].player = False
        # nouvelle position
        self.count += 1
        self.count_ += 1
        self.pos = next_pos
        # cas de base
        if cas is not None:
            setattr(grid[next_pos.x][next_pos.y], cas, False)
    
    
    def ghosts_edit_node(self, pos: Pos2D, next_pos: Pos2D, i: int) -> None:
        """
        Modifie les nodes pour afficher le déplacement des fantômes.
        Il fait également l'actualisation de la position courante. 
        """
        grid = self.board.grid
        # modifie les nodes
        grid[pos.x][pos.y].ghost = False
        grid[next_pos.x][next_pos.y].ghost = True
        # nouvelle position
        self.ghosts[i] = next_pos
    
    
    def ghosts_cond(self, next_pos: Pos2D) -> bool:
        """
        Renvoie True si la position ne se trouve pas sur un item déjà existant.
        """
        if (next_pos not in self.ghosts) and (next_pos not in self.bonuses) and (next_pos != self.end):
            return True