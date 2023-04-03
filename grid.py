"""
Titre : Projet d'année n°2, Dungeon Crawler.
Auteur : Jawad Cherkaoui
Date : 2023-04-02
Matricule : 576517
But : Deux class se chargeant, à deux, de la représentation du donjon à travers une matrice de node.
"""

# importation des modules :
import random
from box import Box
from pos2d import Pos2D
#########################


class Node:
    
    def __init__(self) -> None:
        """
        Construit un noeud représentant une case du donjon.
        """
        # mouvements
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        # en jeu
        self.bonus = False
        self.player = False
        self.end = False
        self.ghost = False
        self.visibility = False

# ----------

class Grid:

    def __init__(self, width: int, height: int) -> None:
        """
        Construit une grille par défaut qui est vide, hormis les murs formant le contour
        """
        self.width = width
        self.height = height
        self.grid = [[Node() for _ in range(height)] for _ in range(width)]    # matrice de Node
        self.isolate_box(Box(Pos2D(0, 0), Pos2D(width - 1, height - 1)))       # isole la boite principale
        self.marked = [[False for _ in range(self.height)] for _ in range(self.width)]


    def add_wall(self, pos1: Pos2D, pos2: Pos2D) -> None:
        """
        Ajoute un mur entre les positions pos1 et pos2 si ces deux cases sont adjacentes.
        """
        if not self.wall_checker(pos1, pos2):
            direction = self.get_direction(pos1, pos2)  # detecte la direction entre les deux positions
            nodePos1 = self.grid[pos1.x][pos1.y]        # recupere le node de la position 1
            nodePos2 = self.grid[pos2.x][pos2.y]        # recupere le node de la position 2
            setattr(nodePos1, direction, False)         # ajoute le mur entre les deux positions
            setattr(nodePos2, self.opposite(direction), False)


    def remove_wall(self, pos1: Pos2D, pos2: Pos2D) -> None:
        """
        Retire un mur entre les positions pos1 et pos2 si ces deux cases sont adjacentes.
        """
        if self.wall_checker(pos1, pos2):
            direction = self.get_direction(pos1, pos2)  # detecte la direction entre les deux positions
            nodePos1 = self.grid[pos1.x][pos1.y]        # recupere le node de la position 1
            nodePos2 = self.grid[pos2.x][pos2.y]        # recupere le node de la position 2
            setattr(nodePos1, direction, True)          # retire le mur entre les deux positions
            setattr(nodePos2, self.opposite(direction), True)


    def isolate_box(self, box: Box) -> None:
        """
        Isole une boite du donjon en ajoutant des murs autour de celle-ci. 
        """
        (x1, x2), (y1, y2) = box.width(), box.height()
         # murs formant le contour au-dessus et en-dessous :
        for i in range(x1, x2 + 1):
            self.add_wall(Pos2D(i, y1), Pos2D(i, y1 - 1)) if y1 - 1 >= 0 \
            else setattr(self.grid[i][y1], 'up', False)
            ###
            self.add_wall(Pos2D(i, y2), Pos2D(i, y2 + 1)) if y2 + 1 < self.height \
            else setattr(self.grid[i][y2], 'down', False)
        # murs formant le contour à gauche et à droite :
        for j in range(y1, y2 + 1): 
            self.add_wall(Pos2D(x1, j), Pos2D(x1 - 1, j)) if x1 - 1 >= 0 \
            else setattr(self.grid[x1][j], 'left', False)
            ###
            self.add_wall(Pos2D(x2, j), Pos2D(x2 + 1, j)) if x2 + 1 < self.width \
            else setattr(self.grid[x2][j], 'right', False)


    def accessible_neighbours(self, pos: Pos2D) -> list[Pos2D]:
        """
        Renvoie une liste contenant toutes les cases accessibles depuis pos.
        """
        if self.dimension_checker(pos):                        
            neighbours = [Pos2D(pos.x, pos.y - 1),  # up       # voisins de (pos) contenus dans (neighbours)
                          Pos2D(pos.x, pos.y + 1),  # down     # return ceux qui remplissent les conditions 
                          Pos2D(pos.x - 1, pos.y),  # left     # cond: dimension_checker, wall_checker
                          Pos2D(pos.x + 1, pos.y)]  # right    
            return [i for i in neighbours if self.dimension_checker(i) and not self.wall_checker(pos, i)]   
        raise ValueError('Invalid position')


    def spanning_tree(self) -> 'Grid':
        """
        Extrait un arbre couvrant aléatoire de la grille.
        """
        visited = []
        board = self.copy()
        copy_marked = self.copy_marked()
        self.dfs(board, Pos2D(0, 0), visited, copy_marked)  # création du chemin (positions dans 'visited')
        # fermeture de toutes les cases du chemin
        for pos in visited:
            for direction in 'up', 'left', 'down', 'right':
                setattr(board.grid[pos.x][pos.y], direction, False)
        # suppression des murs entre les cases du chemin
        for pos in range(1, len(visited)):
            previous = pos-1
            if board.is_adjacent(visited[pos], visited[previous]):
                board.remove_wall(visited[pos], visited[previous])
            else:
                # BACKTRACKING
                # cherche la case précédente adjacente à la case courante
                found = False
                while previous > 0 and not found:
                    if board.is_adjacent(visited[pos], visited[previous]):
                        board.remove_wall(visited[pos], visited[previous])
                        found = True
                    previous -= 1
        return board


    def dfs(self, board: 'Grid', pos: Pos2D, visited: list, marked: list) -> None:
        """
        Remplissage de la liste 'visited' avec les positions du chemin générer par l'algorithme DFS.
        """
        visited.append(pos)                             # ajouts positions du chemin
        marked[pos.x][pos.y] = True                     # marquage
        neighbours = self.accessible_neighbours(pos)    
        random.shuffle(neighbours)                      # parcours des voisins
        for neighbour in neighbours:                    # pas marqués -> rappel la fct
            if not marked[neighbour.x][neighbour.y]:    
                self.dfs(board, neighbour, visited, marked)


    # ----- FONCTIONS HELPER ----- 


    def __add__(self, board: 'Grid') -> 'Grid':
        """
        Renvoie un nouveau donjon qui est la somme des deux donjons.
        Nécessaire pour l'union des deux arbres couvrants.
        """
        if (self.width, self.height) == (board.width, board.height):
            new_grid = Grid(self.width, self.height)
            for x in range(self.width):
                for y in range(self.height):
                    for direction in 'up', 'down', 'left', 'right':
                        if not getattr(self.grid[x][y], direction) and not getattr(board.grid[x][y], direction):
                            setattr(new_grid.grid[x][y], direction, False)
            return new_grid
        raise ValueError('Grids are not the same size')


    def copy(self) -> 'Grid':
        """
        Renvoie la copie de la grille courante.
        """
        new_grid = Grid(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):                               # si le mur est présent, on l'ajoute
                if not self.grid[x][y].up and y != 0:                       # mur supérieur
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x, y - 1))
                if not self.grid[x][y].down and y != self.height - 1:       # mur inférieur
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x, y + 1))
                if not self.grid[x][y].left and x != 0:                     # mur gauche
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x - 1, y))
                if not self.grid[x][y].right and x != self.width - 1:       # mur droit
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x + 1, y))
        return new_grid


    def copy_marked(self) -> list[list[bool]]:
        """
        Renvoie la copie de la liste 'marked' pour éviter les problèmes de références.
        Nécessaire pour la création de deux arbres couvrants différents.
        """
        new_marked = []
        for x in range(self.width):
            new_marked.append([])
            for y in range(self.height):
                if self.marked[x][y] == False:
                    new_marked[x].append(False)
                else:
                    new_marked[x].append(True)
        return new_marked


    def get_direction(self, pos1: Pos2D, pos2: Pos2D) -> str:
        """
        Renvoie la direction entre deux positions.
        """
        if pos1.x == pos2.x:                                    # meme abscisse
            return 'down' if pos1.y +1 == pos2.y else 'up'          # retourne la direction (haut ou bas)
        elif pos1.y == pos2.y:                                  # meme ordonnée
            return 'right' if pos1.x +1 == pos2.x else 'left'       # retourne la direction (gauche ou droite)
        raise ValueError('Positions are not adjacent')


    def opposite(self, direction: str) -> str:
        """
        Renvoie la direction opposée à celle passée en paramètre.
        """
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'right':
            return 'left'
        elif direction == 'left':
            return 'right'


    def is_adjacent(self, pos1: Pos2D, pos2: Pos2D) -> bool:
        """
        Vérifie si deux positions sont adjacentes.
        """
        if abs(pos1.x - pos2.x) == 1 and pos1.y == pos2.y:  # TRUE si la différence entre deux positions est de 1
            return True                                     # et que les deux autres positions ont la même coordonnée
        elif abs(pos1.y - pos2.y) == 1 and pos1.x == pos2.x:
            return True
        return False


    def dimension_checker(self, pos: Pos2D) -> bool:
        """
        Vérifie si une position est valide, donc dans les dimensions du donjon.
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height


    def wall_checker(self, pos1: Pos2D, pos2: Pos2D) -> bool:
        """
        Vérifie si un mur existe entre deux positions.
        """
        if self.dimension_checker(pos1) and self.dimension_checker(pos2):   # verifie si les positions sont valides
            direction = self.get_direction(pos1, pos2)                      # detecte la direction entre les deux positions
            nodePos1 = self.grid[pos1.x][pos1.y]                            # recupere le node de la position 1
            nodePos2 = self.grid[pos2.x][pos2.y]                            # recupere le node de la position 2
            return not getattr(nodePos1, direction) and not getattr(nodePos2, self.opposite(direction))  # check les nodes
        raise ValueError('Invalid position')