"""
Nom : Cherkaoui
Prénom : Jawad
Matricule : 576517
"""

# importation des modules :
import random
from pos2d import Pos2D
from box import Box
#########################


class Node:
    def __init__(self) -> None:
        self.up = True
        self.down = True
        self.left = True
        self.right = True

# --------

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[Node() for _ in range(height)] for _ in range(width)]    # matrice de Node
        self.isolate_box(Box(Pos2D(0, 0), Pos2D(width - 1, height - 1)))       # isole la boite principale


    def __add__(self, board: 'Grid') -> 'Grid':
        if (self.width, self.height) == (board.width, board.height):
            new_grid = Grid(self.width, self.height)
            for x in range(self.width):
                for y in range(self.height):
                    for direction in 'up', 'down', 'left', 'right':
                        if not getattr(self.grid[x][y], direction) and not getattr(board.grid[x][y], direction):
                            setattr(new_grid.grid[x][y], direction, False)
            return new_grid
        raise ValueError('Grids are not the same size')


    def get_direction(self, pos1: Pos2D, pos2: Pos2D) -> str:
        if pos1.x == pos2.x:
            return 'down' if pos1.y +1 == pos2.y else 'up'
        elif pos1.y == pos2.y:
            return 'right' if pos1.x +1 == pos2.x else 'left'
        raise ValueError('Positions are not adjacent')


    def is_adjacent(self, pos1: Pos2D, pos2: Pos2D) -> bool:
        if abs(pos1.x - pos2.x) == 1 and pos1.y == pos2.y:
            return True
        elif abs(pos1.y - pos2.y) == 1 and pos1.x == pos2.x:
            return True
        return False


    def dimension_checker(self, pos: Pos2D) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height


    def wall_checker(self, pos1: Pos2D, pos2: Pos2D) -> bool:
        if self.dimension_checker(pos1) and self.dimension_checker(pos2):   
            direction = self.get_direction(pos1, pos2)
            nodePos1 = self.grid[pos1.x][pos1.y]
            nodePos2 = self.grid[pos2.x][pos2.y]
            if direction == 'up':
                return (nodePos1.up == False) and (nodePos2.down == False)
            elif direction == 'down':
                return (nodePos1.down == False) and (nodePos2.up == False)
            elif direction == 'right':
                return (nodePos1.right == False) and (nodePos2.left == False)
            elif direction == 'left':
                return (nodePos1.left == False) and (nodePos2.right == False)
        raise ValueError('Invalid position')


    def add_wall(self, pos1: Pos2D, pos2: Pos2D) -> None:
        if not self.wall_checker(pos1, pos2):
            direction = self.get_direction(pos1, pos2)
            nodePos1 = self.grid[pos1.x][pos1.y]
            nodePos2 = self.grid[pos2.x][pos2.y]
            if direction == 'up':
                nodePos1.up = False
                nodePos2.down = False
            elif direction == 'down':
                nodePos1.down = False
                nodePos2.up = False
            elif direction == 'right':
                nodePos1.right = False
                nodePos2.left = False
            elif direction == 'left':
                nodePos1.left = False
                nodePos2.right = False


    def remove_wall(self, pos1: Pos2D, pos2: Pos2D) -> None:
        if self.wall_checker(pos1, pos2):
            direction = self.get_direction(pos1, pos2)
            nodePos1 = self.grid[pos1.x][pos1.y]
            nodePos2 = self.grid[pos2.x][pos2.y]
            if direction == 'up':
                nodePos1.up = True
                nodePos2.down = True
            elif direction == 'down':
                nodePos1.down = True
                nodePos2.up = True
            elif direction == 'right':
                nodePos1.right = True
                nodePos2.left = True
            elif direction == 'left':
                nodePos1.left = True
                nodePos2.right = True


    def isolate_box(self, box: Box) -> None:
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
        if self.dimension_checker(pos):                        
            neighbours = [Pos2D(pos.x, pos.y - 1),  # up       # voisins de (pos) contenus dans (neighbours)
                          Pos2D(pos.x, pos.y + 1),  # down     # ceux qui remplissent les conditions 
                          Pos2D(pos.x - 1, pos.y),  # left     # sont contenus dans (accessible_neighbours)
                          Pos2D(pos.x + 1, pos.y)]  # right    
            accessible_neighbours = [i for i in neighbours if self.dimension_checker(i) and not self.wall_checker(pos, i)]   
            return accessible_neighbours
        else:
            raise ValueError('Invalid position')


    def copy(self) -> 'Grid':
        new_grid = Grid(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].up and y != 0:
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x, y - 1))
                if not self.grid[x][y].down and y != self.height - 1:
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x, y + 1))
                if not self.grid[x][y].left and x != 0:
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x - 1, y))
                if not self.grid[x][y].right and x != self.width - 1:
                    new_grid.add_wall(Pos2D(x, y), Pos2D(x + 1, y))
        return new_grid


    def spanning_tree(self) -> 'Grid':
        visited = []
        board = self.copy()
        marked = [[False for _ in range(self.height)] for _ in range(self.width)]
        self.dfs(board, Pos2D(0, 0), visited, marked)  # création du chemin (positions dans 'visited')
        # fermeture de toutes les cases du chemin
        for pos in visited:
            for direction in 'up', 'left', 'down', 'right':
                setattr(board.grid[pos.x][pos.y], direction, False)
        # suppression des murs entre les cases du chemin
        for i in range(1, len(visited)):
            if board.is_adjacent(visited[i], visited[i-1]):
                board.remove_wall(visited[i], visited[i-1])
            else:
                # BACKTRACKING
                previous = i-1
                found = False
                while previous > 0 and not found:
                    if board.is_adjacent(visited[i], visited[previous]):
                        board.remove_wall(visited[i], visited[previous])
                        found = True
                    previous -= 1
        return board


    def dfs(self, board: 'Grid', pos: Pos2D, visited: list, marked: list) -> None:
        visited.append(pos)                             # ajouts positions du chemin
        marked[pos.x][pos.y] = True                     # marquage
        neighbours = self.accessible_neighbours(pos)    
        random.shuffle(neighbours)                      
        for neighbour in neighbours:                    # parcours des voisins
            if not marked[neighbour.x][neighbour.y]:    # pas marqués -> rappel la fct
                self.dfs(board, neighbour, visited, marked)